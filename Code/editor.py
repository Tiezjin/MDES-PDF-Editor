# merge, delete, extract, and split functions 

import os, platform, subprocess
import PyPDF2


class PDFEditorBackend:
    def __init__(self):
        pass

    def _create_outputfile_name(self, input_paths, output_folder_path, function_name, message_queue):
        base_names = [] 
        if len(input_paths) == 1:
            base_name = os.path.splitext(os.path.basename(input_paths[0]))[0]
            truncated_name = base_name[:5]
            base_names.append(truncated_name)
        elif len(input_paths) > 1:
            for path in input_paths:
                base_name = os.path.splitext(os.path.basename(path))[0]
                truncated_name = base_name[:5]
                base_names.append(truncated_name)
        outputfile_name = '-'.join(base_names) + function_name
        outputfile_path = os.path.join(output_folder_path, outputfile_name)
        if len(outputfile_path) > 255:
            message_queue.put((f"The generated output path is too long: {len(outputfile_path)} characters."
                             "Please use shorter input filenames.", True))
            return
        return outputfile_path

    def _parse_page_ranges(self, pages_list, message_queue):
        if not pages_list:
            message_queue.put(("pages_list must be a non-empty list of page numbers or ranges.", True))
            return []
        parsed_pages_list = []
        for item in pages_list:
            if '-' in item:
                try: 
                    start, end = map(int, item.split('-'))
                    if start > end:
                        message_queue.put((f"Invalid page range: {item}. Start page must not be greater than end page.", True))
                    else: 
                        parsed_pages_list.extend(range(start, end+1))
                except ValueError:
                    message_queue.put((f"Invalid page range format: '{item}'. Please use numbers separated by a hyphen(-).", True))
            else:
                try:
                    parsed_pages_list.append(int(item))
                except ValueError:
                    message_queue.put((f"Invalid page number: '{item}'. Please use integers only.", True))
        return parsed_pages_list

    def merge_pdfs(self, input_paths, output_folder_path, message_queue, stop_event):
        try:
            if len(input_paths) < 2:
                message_queue.put(("merge_pdfs() requires at least two input PDF files.", True))
                return
            output_path = self._create_outputfile_name(input_paths, output_folder_path, "_merged.pdf", message_queue)
            pdf_writer = PyPDF2.PdfWriter()
            for pdf in input_paths:
                if stop_event.is_set():
                    message_queue.put(("Merging operation was cancelled by the user.", True))
                    return
                pdf_reader = PyPDF2.PdfReader(pdf)
                pdf_writer.append(pdf_reader)
            with open(output_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)
            self._open_folder(output_folder_path, message_queue)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            message_queue.put((error_message, True))


    def delete_pages(self, input_paths, output_folder_path, pages_list, message_queue, stop_event):
        try:
            if len(input_paths) != 1:
                message_queue.put(("delete_pages() requires exactly one input PDF file.", True))
                return 
            output_path = self._create_outputfile_name(input_paths, output_folder_path, "_deleted.pdf", message_queue)
            parsed_pages_list = self._parse_page_ranges(pages_list, message_queue)
            pdf_writer = PyPDF2.PdfWriter()
            pdf_reader = PyPDF2.PdfReader(input_paths[0])
            for page in range(len(pdf_reader.pages)):
                if stop_event.is_set():
                    message_queue.put(("Deletion operation was cancelled by the user.", True))
                    return
                if (page + 1) not in parsed_pages_list:
                    pdf_writer.add_page(pdf_reader.pages[page])
            with open(output_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)
            self._open_folder(output_folder_path, message_queue)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            message_queue.put((error_message, True))

    def extract_pages(self, input_paths, output_folder_path, pages_list, message_queue, stop_event):
        try:
            if len(input_paths) != 1:
                message_queue.put(("extract_pages() requires exactly one input PDF file.", True))
                return
            output_path = self._create_outputfile_name(input_paths, output_folder_path, "_extracted.pdf", message_queue)
            parsed_pages_list = self._parse_page_ranges(pages_list, message_queue)
            pdf_writer = PyPDF2.PdfWriter()
            pdf_reader = PyPDF2.PdfReader(input_paths[0])
            for page in range(len(pdf_reader.pages)):
                if stop_event.is_set():
                    message_queue.put(("Extraction operation was cancelled by the user.", True))
                    return
                if (page + 1) in parsed_pages_list:
                    pdf_writer.add_page(pdf_reader.pages[page])
            with open(output_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)
            self._open_folder(output_folder_path, message_queue)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            message_queue.put((error_message, True))

    def split_pdfs(self, input_paths, output_folder_path, pages_list, message_queue, stop_event):
        try:
            if len(input_paths) != 1:
                message_queue.put(("split_pdfs() requires exactly one input PDF file.", True))
                return
            pdf_reader = PyPDF2.PdfReader(input_paths[0])
            parsed_pages_list = self._parse_page_ranges(pages_list, message_queue)
            split_points = sorted(list(set([1] + parsed_pages_list + [len(pdf_reader.pages) + 1])))
            for i in range(len(split_points) - 1):
                if stop_event.is_set():
                    message_queue.put(("Splitting operation was cancelled by the user.", True))
                    return
                start_1_indexed = split_points[i]
                end_1_indexed = split_points[i + 1]
                pdf_writer = PyPDF2.PdfWriter()
                for page in pdf_reader.pages[start_1_indexed-1:end_1_indexed-1]:
                    pdf_writer.add_page(page)
                output_path = self._create_outputfile_name(input_paths, output_folder_path, f"_part{i}.pdf", message_queue)
                with open(output_path, "wb") as output_pdf:
                    pdf_writer.write(output_pdf)
            self._open_folder(output_folder_path, message_queue)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            message_queue.put((error_message, True))

    def _open_folder(self, output_folder_path, message_queue):
        try:
            if platform.system() == "Windows":
                os.startfile(output_folder_path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", output_folder_path])
            else:
                subprocess.run(["xdg-open", output_folder_path])
            message_queue.put(("Operation finished!", False))
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            message_queue.put((f"Could not open the output folder: {e}", True))
            return 
        except Exception as e:
            message_queue.put((f"Could not open file: {e}", True))
            return 