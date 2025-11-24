import pandas as pd
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(33, 37, 41) # Dark gray
        self.cell(0, 10, 'PainScout.ai Intelligence Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()} | Powered by Gemini AI', 0, 0, 'C')

class Reporter:
    @staticmethod
    def generate_pdf(df: pd.DataFrame, summary_stats: dict) -> bytes:
        pdf = PDFReport()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Title Section
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d')}", 0, 1)
        pdf.ln(5)
        
        # Executive Summary
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(41, 98, 255) # Brand Blue
        pdf.cell(0, 10, "Executive Summary", 0, 1)
        pdf.set_text_color(0)
        pdf.set_font('Arial', '', 11)
        
        pdf.multi_cell(0, 7, f"PainScout.ai analyzed {summary_stats['total_posts']} discussions across Reddit and X to identify high-value B2B opportunities. The analysis reveals a strong demand for solutions in the '{summary_stats['top_category']}' sector.")
        pdf.ln(2)
        pdf.multi_cell(0, 7, f"We detected {summary_stats['high_urgency_count']} critical pain points that users described with high frustration. These represent immediate revenue opportunities for SaaS founders ready to build targeted solutions.")
        pdf.ln(10)
        
        # Top Pain Points Table
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(41, 98, 255)
        pdf.cell(0, 10, "Top Detected Opportunities", 0, 1)
        pdf.set_text_color(0)
        
        # Headers
        pdf.set_font('Arial', 'B', 10)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(90, 10, "Pain Point", 1, 0, 'L', 1)
        pdf.cell(40, 10, "Category", 1, 0, 'L', 1)
        pdf.cell(30, 10, "Urgency", 1, 0, 'C', 1)
        pdf.cell(30, 10, "Score", 1, 1, 'C', 1)
        
        # Rows (Top 10)
        pdf.set_font('Arial', '', 9)
        top_df = df.sort_values(by='sentiment_score', ascending=False).head(10)
        
        for _, row in top_df.iterrows():
            pain = str(row.get('pain_point', 'N/A'))[:50] + "..."
            cat = str(row.get('category', 'N/A'))[:20]
            urgency = str(row.get('urgency', '-'))
            score = str(row.get('sentiment_score', 0))
            
            pdf.cell(90, 8, pain, 1)
            pdf.cell(40, 8, cat, 1)
            pdf.cell(30, 8, urgency, 1, 0, 'C')
            pdf.cell(30, 8, score, 1, 1, 'C')
            
        return pdf.output(dest='S').encode('latin-1')

    @staticmethod
    def get_csv_download_link(df: pd.DataFrame):
        return df.to_csv(index=False).encode('utf-8')
