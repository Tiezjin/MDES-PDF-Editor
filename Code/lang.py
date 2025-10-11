# management of langauage and translation

class LanguageManager:
    def __init__(self):
        self.current_lang = 'English'  
        self.translations = {
            'English': {
                'Welcome_info': 
                    """Hello, welcome to PDF Editor built entirely in Python!
                    PDF Editor - Quick Guide
                    •Select PDF - Choose input file
                    •Choose Folder - Select output destination
                    •Pick Function - Merge, Delete, Extract, or Split
                    That's it! The selected folder will open automatically.
                    PS:
                    • MERGE: Combine multiple PDFs (no page ranges needed)
                    • EXTRACT/DELETE: Use 1, 3-5, 6 (includes these pages)
                    • SPLIT: Use 5, 9, 12 (splits before these pages)""",
                # UI
                'label_title': 'PDF Editor',
                'label_input_pdfs':'Input PDFs', 
                'label_output_folder': 'Output Folder', 
                'label_page_ranges': 'Page Ranges',
                'label_page_range_example':'for example, 1, 12-15, 17',
                'label_message_box': 'Info Dashboard',
                'button_add_pdfs': 'Add PDFs',
                'button_browse_folder': 'Browse Folder',
                'merge': 'Merge',
                'delete': 'Delete',
                'extract': 'Extract',
                'split': 'Split',
                'stop': 'Stop',
                'title_add_pdfs': 'Select PDF Files',
                'title_browse_folder': 'Select an Output Folder',
                # exception handling
                'error_not_input_paths': 'Missing input PDFs.',
                'error_not_output_folder': 'Missing output folder.',
                'error_not_page_ranges': 'Missing page ranges.',
                # update status
                'status_with_page_range': """
                    PDF operation starts ...
                    Input paths: {input_paths} 
                    Output folder: {output_folder} 
                    Page ranges: {page_ranges}""",
                'status_no_page_range': 
                    """PDF operation starts ...
                    Input paths: {input_paths} 
                    Output folder: {output_folder}""",
                'status_stop': 'Stopping operation...',
                'stop_msg': 'Operation finished!',
            },

            '中文': {
                'welcome_info': 
                (
                "你好，欢迎使用完全用Python构建的PDF编辑器！\n"
                "PDF编辑器 - 快速指南\n"
                "•选择PDF - 选择输入文件\n"
                "•选择文件夹 - 选择输出目标\n"
                "•选择功能 - 合并、删除、提取或拆分\n"
                "就是这样！所选文件夹将自动打开。\n"
                "PS：\n"
                "• 合并：合并多个PDF（无需页面范围）\n"
                "• 提取/删除：使用1、3-5、6（包括这些页面）\n"
                "• 拆分：使用5、9、12（在这些页面之前拆分）"
                ),
                # ui
                'label_title': "PDF 编辑器",
                'label_input_pdfs': '输入PDF',
                'label_output_folder': '输出文件夹',
                'label_page_ranges': '页面范围',
                'label_page_range_example':'例如，1、12-15、17',
                'label_message_box': '信息面板',
                'button_add_pdfs': '添加PDF',
                'button_browse_folder': '浏览文件夹',
                'merge': '合并',
                'delete': '删除',
                'extract': '提取',
                'split': '拆分',
                'stop': '停止',
                # exception handling
                'error_not_input_paths': '缺少输入PDF。',
                'error_not_output_folder': '缺少输出文件夹。',
                'error_not_page_ranges': '缺少页面范围。',
                # update status
                'status_with_page_range': (
                    "PDF操作开始...\n"
                    "输入路径: {input_paths}\n"
                    "输出文件夹: {output_folder}\n"
                    "页面范围: {page_ranges}"
                ),
                'status_no_page_range': (
                    "PDF操作开始...\n"
                    "输入路径: {input_paths}\n"
                    "输出文件夹: {output_folder}"
                ),
                'status_stop': '正在停止操作...',
                'stop_msg': '操作完成！',
            },

            'Deutsch': {
                'welcome_info': (
                "Hallo, willkommen beim vollständig in Python erstellten PDF-Editor!\n"
                "PDF-Editor - Schnellübersicht\n"
                "•PDF auswählen - Eingabedatei wählen\n"
                "•Ordner wählen - Ausgabeverzeichnis auswählen\n"
                "•Funktion wählen - Zusammenführen, Löschen, Extrahieren oder Teilen\n"
                "Das war's! Der gewählte Ordner öffnet sich automatisch.\n"
                "PS:\n"
                "• ZUSAMMENFÜGEN: Mehrere PDFs kombinieren (keine Seitenbereiche erforderlich)\n"
                "• EXTRAHIEREN/LÖSCHEN: Verwenden Sie 1, 3-5, 6 (einschließlich dieser Seiten)\n"
                "• TEILEN: Verwenden Sie 5, 9, 12 (vor diesen Seiten teilen)"
                ),
                'label_title': "PDF Editor",
                'label_input_pdfs': 'PDFs hinzufügen',
                'label_output_folder': 'Ordner durchsuchen',
                'label_page_ranges': 'Seitenbereiche',
                'button_add_pdfs': 'PDFs hinzufügen',
                'button_browse_folder': 'Ordner durchsuchen',
                'merge': 'Zusammenführen',
                'delete': 'Löschen',
                'extract': 'Extrahieren',
                'split': 'Teilen',
                'stop': 'Stopp',
                # exception handling
                'error_not_input_paths': 'Eingabe-PDFs fehlen.',
                'error_not_output_folder': 'Ausgabeordner fehlt.',
                'error_not_page_ranges': 'Seitenbereiche fehlen.',
                # update status
                'status_with_page_range': (
                "PDF-Vorgang startet ...\n"
                "Eingabepfade: {input_paths}\n"
                "Ausgabeordner: {output_folder}\n"
                "Seitenbereiche: {page_ranges}"
                ),
                'status_no_page_range': (
                "PDF-Vorgang startet ...\n"
                "Eingabepfade: {input_paths}\n"
                "Ausgabeordner: {output_folder}"
                ),
                'status_stop': 'Vorgang wird gestoppt...',
                'stop_msg': 'Vorgang abgeschlossen!',
            }
        }

    def set_lang(self, lang_abbr):
        """Change language dynamically"""
        if lang_abbr in self.translations:
            self.current_lang = lang_abbr

    def trans(self, key):
        lang_dict = self.translations.get(self.current_lang, {})
        return lang_dict.get(key, key)