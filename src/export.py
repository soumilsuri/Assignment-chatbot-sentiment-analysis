"""
Export functionality for conversations and analysis results.
Supports PDF, CSV, and JSON formats.
"""

import json
import csv
import io
from datetime import datetime
from typing import Dict, List, Optional, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class ConversationExporter:
    def __init__(self):
        pass
    
    def export_to_json(self, conversation_history: List[Dict[str, str]], 
                      analysis_results: Optional[Dict[str, Any]] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> str:
        export_data = {
            'metadata': metadata or {
                'export_date': datetime.now().isoformat(),
                'version': '1.0'
            },
            'conversation': conversation_history,
            'analysis': analysis_results
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def export_to_csv(self, conversation_history: List[Dict[str, str]],
                     sentiment_results: Optional[List[Dict[str, Any]]] = None) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Message Number', 'Role', 'Message', 'Sentiment', 'Score', 'Confidence'])
        
        user_msg_index = 0
        for i, msg in enumerate(conversation_history):
            row = [i + 1, msg['role'], msg['content']]
            
            if msg['role'] == 'user' and sentiment_results and user_msg_index < len(sentiment_results):
                sent = sentiment_results[user_msg_index]
                row.extend([
                    sent.get('label', 'N/A'),
                    sent.get('score', 'N/A'),
                    f"{sent.get('confidence', 0):.2%}"
                ])
                user_msg_index += 1
            else:
                row.extend(['N/A', 'N/A', 'N/A'])
            
            writer.writerow(row)
        
        return output.getvalue()
    
    def export_to_pdf(self, conversation_history: List[Dict[str, str]],
                     analysis_results: Optional[Dict[str, Any]] = None,
                     sentiment_results: Optional[List[Dict[str, Any]]] = None) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Conversation Analysis Report", title_style))
        story.append(Spacer(1, 12))
        
        meta_style = ParagraphStyle(
            'Meta',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey
        )
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", meta_style))
        story.append(Spacer(1, 20))
        
        if analysis_results:
            story.append(Paragraph("Overall Analysis", styles['Heading2']))
            
            overall = analysis_results.get('overall_sentiment', {})
            if overall:
                score = overall.get('score', 'N/A')
                label = overall.get('label', 'N/A').capitalize()
                confidence = overall.get('confidence', 0)
                
                analysis_text = f"""
                <b>Sentiment:</b> {label}<br/>
                <b>Score:</b> {score}/100<br/>
                <b>Confidence:</b> {confidence:.1%}<br/>
                """
                story.append(Paragraph(analysis_text, styles['Normal']))
                story.append(Spacer(1, 12))
        
        story.append(PageBreak())
        
        story.append(Paragraph("Conversation History", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        table_data = [['#', 'Role', 'Message', 'Sentiment', 'Score']]
        
        user_msg_index = 0
        for i, msg in enumerate(conversation_history):
            role = msg['role'].capitalize()
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            
            if msg['role'] == 'user' and sentiment_results and user_msg_index < len(sentiment_results):
                sent = sentiment_results[user_msg_index]
                sentiment = sent.get('label', 'N/A').capitalize()
                score = sent.get('score', 'N/A')
                user_msg_index += 1
            else:
                sentiment = '-'
                score = '-'
            
            table_data.append([str(i + 1), role, content, sentiment, str(score)])
        
        table = Table(table_data, colWidths=[0.5*inch, 1*inch, 4*inch, 1*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(table)
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

