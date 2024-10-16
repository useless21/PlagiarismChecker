import re
import flet as flt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from win32api import GetSystemMetrics
import win32gui

# Function to tokenize the code (a simple example)

def myapp(page: flt.Page):
    # Initialise page criteria and components
    page.theme_mode = flt.ThemeMode.LIGHT
    page.window.maximized=True
    page.on_resized=lambda e: on_resize()
    page.scroll=True
    # page.window_left = -10
    # page.window_top = 0
    # page.window_height = GetSystemMetrics(1) - 30
    # page.window_width = GetSystemMetrics(0) + 30

    global methods, method1, data1, cl1, runner,allowed
    allowed=["py"]
    runner = 0
    file_picker = flt.FilePicker()
    page.overlay.append(file_picker)
    isi=flt.RadioGroup(content=flt.Column([
    flt.Radio(value=1, label="Text"),
    flt.Radio(value=2, label="Upload")]),value=1,on_change=lambda e: radiogroup_changed(e))

    methods=flt.RadioGroup(content=flt.Row([
        flt.Radio(value=1, label='Python'),
        flt.Radio(value=2, label='C++   '),
        flt.Radio(value=3, label='C#    '),
        flt.Radio(value=4, label='Java  '),
        flt.Radio(value=5, label='C     '),
        flt.Radio(value=6, label='Kotlin')]),value=1,on_change=lambda e: meth_change())
    # dv = flt.Column([methods], scroll=True)
    # meth = flt.Row([dv], scroll=True, expand=1, vertical_alignment=flt.CrossAxisAlignment.START)
    # method1 =
    data1 = flt.TextField(
        label="Code 1",
        value="",
        hint_text="eg. 12 14 15 18 24...",
        helper_text="Original Code",
        tooltip="Enter integers separated by spaces",
        multiline=True,
        width=(page.width-50)/2,
    )
    cl1 = flt.TextField(
        label="Code 2",
        value="",
        hint_text="eg. 8",
        helper_text="Code to be checked",
        tooltip="Enter a single integer for cache line number",
        multiline=True,
        width=(page.width-50) / 2,
    )
    select=flt.ElevatedButton(
        "Select files...",
        icon=flt.icons.FOLDER_OPEN,
        on_click=lambda e: file_picker.pick_files(allow_multiple=True,allowed_extensions=allowed),
        visible=False
    )

    butang = flt.ElevatedButton(text="Submit", on_click=lambda e: process())
    alr = flt.Column(
        controls=[
            flt.Text(
                "This software is designed to help users compare code snippets or entire files to check for plagiarism or similarity. It uses a method called TF-IDF (Term Frequency-Inverse Document Frequency) to analyze the tokens (words, operators, etc.) from different pieces of code and computes the cosine similarity between them. This similarity score indicates how closely the two pieces of code resemble each other.\n"
            ),
            flt.Text("Features:\n", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
            flt.Text(
                spans=[
                    flt.TextSpan("Code Comparison: ", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
                    flt.TextSpan(
                        "You can either enter two code snippets manually or upload files containing the code you want to compare.")
                ]
            ),
            flt.Text(
                spans=[
                    flt.TextSpan("Plagiarism Detection: ", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
                    flt.TextSpan(
                        "After the comparison, the software will compute a similarity score that ranges from 0 to 1. A score closer to 1 indicates that the codes are very similar, while a score closer to 0 indicates less similarity.")
                ]
            ),
            flt.Text(
                spans=[
                    flt.TextSpan("Multiple Programming Languages: ", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
                    flt.TextSpan(
                        "You can choose the programming language of the code you're comparing, and the software will adapt accordingly.")
                ]
            ),
            flt.Text(
                spans=[
                    flt.TextSpan("Interactive UI: ", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
                    flt.TextSpan(
                        "The user interface allows switching between Light and Dark themes, file selection, and real-time similarity processing.\n")
                ]
            ),
            flt.Text("How to Use:\n", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
            flt.Text(
                spans=[
                    flt.TextSpan("Text: ", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
                    flt.TextSpan("Input code directly into text fields.")
                ]
            ),
            flt.Text(
                spans=[
                    flt.TextSpan("Upload: ", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
                    flt.TextSpan("Select multiple code files (with .py extension) from your system to compare.")
                ]
            ),
            flt.Text(
                spans=[
                    flt.TextSpan("Choosing Programming Language: ", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
                    flt.TextSpan(
                        "Select the programming language of the code you are working with from the available options (e.g., Python, C++, etc.).")
                ]
            ),
            flt.Text(
                spans=[
                    flt.TextSpan("Enter or Upload Code: ", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
                    flt.TextSpan(
                        "If you choose Text, fill the text fields with the code you want to compare. If you choose Upload, select the files from your system using the \"Select files\" button.")
                ]
            ),
            flt.Text(
                spans=[
                    flt.TextSpan("Compare: ", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
                    flt.TextSpan(
                        "Once you have provided the code, click the Submit button to process the comparison. The similarity score will be displayed in a table.")
                ]
            ),
            flt.Text(
                spans=[
                    flt.TextSpan("View Results: ", style=flt.TextStyle(weight=flt.FontWeight.BOLD)),
                    flt.TextSpan(
                        "After submission, a table will show the similarity score between the code snippets or files you have provided, indicating how similar the two codes are.")
                ]
            ),
        ]
    )

    dlg = flt.AlertDialog(
        title=flt.Text("Welcome to our Code Plagiarism Checker"),
        content=flt.Column([alr],scroll=flt.ScrollMode.ADAPTIVE),
    )
    # methods.horizontal_lines = flt.border.BorderSide(2, "#fdfcff")
    page.update()
    def theme_changed(e):
        page.theme_mode = (
            flt.ThemeMode.DARK
            if page.theme_mode == flt.ThemeMode.LIGHT
            else flt.ThemeMode.LIGHT
        )
        switch.label = (
            "Light theme" if page.theme_mode == flt.ThemeMode.LIGHT else "Dark theme"
        )
        page.update()

    page.theme_mode = flt.ThemeMode.LIGHT
    switch = flt.Switch(label="Light theme", on_change=theme_changed)
    help = flt.Row([
        flt.Column([
            flt.Container(
                switch, alignment=flt.alignment.top_left,
            ),
        ]),
        flt.Column([
            flt.Container(
                content=flt.ElevatedButton("Help", on_click=lambda e: open_dlg()),
                padding=5, alignment=flt.alignment.center
            ),
        ]),
    ],
        alignment=flt.MainAxisAlignment.SPACE_BETWEEN
    )
    global scr
    scr = flt.Row([
        flt.Column([
            flt.Container(
                data1, alignment=flt.alignment.center_left,
            ),
        ]),
        flt.Column([
            flt.Container(
                cl1, alignment=flt.alignment.center_right,
            ),
        ]),
    ],
        alignment=flt.MainAxisAlignment.CENTER
    )


    # scr.controls.append(data1)
    # scr.controls.append(cl1)
    # scr.controls.append(method1)
    # scr.controls.append(labels)
    page.add(help,methods,isi,scr,select,butang)
    def meth_change():
        global methods,allowed
        if int(methods.value) == 1:
            allowed=["py"]

        elif int(methods.value) == 2:
            print("cpp")
            allowed = ["cpp"]

        elif int(methods.value) == 3:
            allowed = ["cs"]

        elif int(methods.value) == 4:
            allowed = ["java"]

        elif int(methods.value) == 5:
            allowed = ["c"]

        elif int(methods.value) == 6:
            allowed = ["kt"]

    def tokenize_code(code):
        global methods
        # Remove comments
        if int(methods.value) == 1:
            print("python")
            code = re.sub(r'#[^\n]*', '', code)  # Removes Python comments
            # Remove string literals
            code = re.sub(r'".*?"', '""', code)  # Removes strings in double quotes
            code = re.sub(r"'.*?'", "''", code)  # Removes strings in single quotes
            # Keep only alphanumeric characters and some basic operators
            tokens = re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*|\S', code)
            return ' '.join(tokens)

        elif int(methods.value) == 2:
            print("cpp")
            # Remove single-line comments (//) and multi-line comments (/* */)
            code = re.sub(r'//[^\n]*', '', code)  # Removes single-line comments
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Removes multi-line comments
            # Remove string literals
            code = re.sub(r'".*?"', '""', code)  # Removes strings in double quotes
            code = re.sub(r"'.*?'", "''", code)  # Removes characters in single quotes
            # Keep only alphanumeric characters and some basic operators
            tokens = re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*|\S', code)
            return ' '.join(tokens)


        elif int(methods.value) == 3:
            # Remove single-line comments (//) and multi-line comments (/* */)
            code = re.sub(r'//[^\n]*', '', code)  # Removes single-line comments
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Removes multi-line comments
            # Remove string literals
            code = re.sub(r'".*?"', '""', code)  # Removes strings in double quotes
            code = re.sub(r"'.*?'", "''", code)  # Removes characters in single quotes
            # Keep only alphanumeric characters and some basic operators
            tokens = re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*|\S', code)
            return ' '.join(tokens)


        elif int(methods.value) == 4:
            # Remove single-line comments (//) and multi-line comments (/* */)
            code = re.sub(r'//[^\n]*', '', code)  # Removes single-line comments
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Removes multi-line comments
            # Remove string literals
            code = re.sub(r'".*?"', '""', code)  # Removes strings in double quotes
            code = re.sub(r"'.*?'", "''", code)  # Removes characters in single quotes
            # Keep only alphanumeric characters and some basic operators
            tokens = re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*|\S', code)
            return ' '.join(tokens)


        elif int(methods.value) == 5:
            # Remove single-line comments (//) and multi-line comments (/* */)
            code = re.sub(r'//[^\n]*', '', code)  # Removes single-line comments
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Removes multi-line comments
            # Remove string literals
            code = re.sub(r'".*?"', '""', code)  # Removes strings in double quotes
            code = re.sub(r"'.*?'", "''", code)  # Removes characters in single quotes
            # Keep only alphanumeric characters and some basic operators
            tokens = re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*|\S', code)
            return ' '.join(tokens)


        elif int(methods.value) == 6:
            # Remove single-line comments (//) and multi-line comments (/* */)
            code = re.sub(r'//[^\n]*', '', code)  # Removes single-line comments
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Removes multi-line comments
            # Remove string literals
            code = re.sub(r'".*?"', '""', code)  # Removes strings in double quotes
            code = re.sub(r"'.*?'", "''", code)  # Removes characters in single quotes
            # Keep only alphanumeric characters and some basic operators
            tokens = re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*|\S', code)
            return ' '.join(tokens)



    # Function to compute the plagiarism similarity between two code snippets
    def compute_similarity(code1, code2):
        # Tokenize both code snippets
        code1_tokens = tokenize_code(code1)
        code2_tokens = tokenize_code(code2)

        # Use TF-IDF Vectorizer to convert code to vectors
        vectorizer = TfidfVectorizer()
        vect_mat=vectorizer.fit_transform([code1_tokens, code2_tokens])
        print("TF-IDF Vocabulary:")
        print(vectorizer.vocabulary_)
        df = pd.DataFrame(vectorizer.transform([code1_tokens, code2_tokens]).toarray(), columns=vectorizer.get_feature_names_out())
        print(df)
        # Compute the cosine similarity between the vectors
        similarity_matrix = cosine_similarity(vect_mat)
        print("similarity_matrix")
        print(similarity_matrix)
        return similarity_matrix[0][1]  # Returns the similarity score between code1 and code2

    def open_dlg():
        page.overlay.append(dlg)
        dlg.open = True
        page.update()
    def on_resize():
        data1.width = (page.window.width-50)/2
        cl1.width = (page.window.width-50) /2
        page.update()

    prog_bars: dict[str, flt.ProgressRing] = {}
    files = flt.Ref[flt.Column]()

    def file_clear_result(e: flt.FilePickerResultEvent):
        prog_bars.clear()
        files.current.controls.clear()
    def file_picker_result(e: flt.FilePickerResultEvent):
        global nama,bulat
        prog_bars.clear()
        files.current.controls.clear()
        if files is not None:
            nama=e.files
            for f in e.files:
                prog = flt.ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                prog_bars[f.name] = prog
                # Add the progress ring and file name to the UI
                bulat=flt.Row([prog, flt.Text(f.name)])
                files.current.controls.append(bulat)

            # Make sure the page is updated after adding progress rings
            page.update()
        print(files)
            # Automatically trigger the file upload after files are selected
        upload_files()



    def process():
        row=0
        mastlst=[]
        tbllst = []
        if int(isi.value)==2:
            count=0
            print(nama[0].path)
            for i in nama:
                print(i)
                file_path = i.path
                print(file_path)
                with open(file_path, 'r') as file:
                    page.session.set(str(count), file.read())
                count=count+1


            for i in range(len(nama)):
                for j in range(i + 1, len(nama)):
                    print(f"Comparing '{nama[i].name}' with '{nama[j].name}'")
                    tbllst.insert(0,nama[i].name)
                    tbllst.insert(1,nama[j].name)
                    #Compare logic TFIDF
                    similarity_score=compute_similarity(page.session.get(str(i)), page.session.get(str(j)))
                    print(f"Plagiarism Similarity Score: {similarity_score:.2f}")
                    tbllst.insert(2,str(round(similarity_score*100, 2))+"%")
                    print(row)
        if int(isi.value) == 1:
            for i in range(2):
                for j in range(i + 1, 2):
                    tbllst.insert(0,"Code 1")
                    tbllst.insert(1,"Code 2")
                    #Compare logic TFIDF
                    similarity_score=compute_similarity(data1.value, cl1.value)
                    print(f"Plagiarism Similarity Score: {similarity_score:.2f}")
                    tbllst.insert(2,round(similarity_score, 2))
                    print(row)

        mastlst.append(tbllst)
        Maketbl(row,mastlst)


        page.update()
    def on_upload_progress(e: flt.FilePickerUploadEvent):
        if e.file_name in prog_bars:
            # Update the progress ring value
            prog_bars[e.file_name].value = e.progress
            prog_bars[e.file_name].update()

    file_picker = flt.FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)
    def radiogroup_changed(e):
        if e.control.value == "1":
            data1.visible=True
            cl1.visible = True
            select.visible=False
            file_clear_result(e)

            print("Masuk 1")
        if e.control.value == "2":
            data1.visible = False
            cl1.visible = False
            select.visible=True
            file_clear_result(e)
            print("Masuk 2")
        else:
            print(type(e.control.value))
        print("Done")
        page.update()

    def Maketbl(row,mastlst):
        global runner,oldt
        panjang=3
        mastlst = [mastlst[0][i:i + panjang] for i in range(0, len(mastlst[0]), panjang)]
        print("Master List")
        print(mastlst)
        print(type(isi.value))
        if int(isi.value)==1:
            header_names=["Code 1","Code 2","Score"]
        if int(isi.value)==2:
            header_names=["File 1","File 2","Score"]
        col = [flt.DataColumn(flt.Text(header)) for header in header_names]
        print(col)
        table_rows = []
        for row in mastlst:
            table_rows.append(
                flt.DataRow(cells=[
                    flt.DataCell(flt.Text(str(item))) for item in row
                ])
            )
        dt = flt.DataTable(heading_text_style=flt.TextStyle(weight=flt.FontWeight.BOLD, color="black"),
                           heading_row_color=flt.colors.AMBER_50, columns=col, rows=table_rows)
        cv = flt.Column([dt], scroll=True)
        scrollt = flt.Row([cv], scroll=flt.ScrollMode.ADAPTIVE, expand=1, vertical_alignment=flt.CrossAxisAlignment.START)
        page.add(scrollt)
        if runner>0:
            print("buang")
            page.remove(oldt)
        oldt=scrollt
        runner=runner+1
        page.update()
    def upload_files():
        uf = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                uf.append(
                    flt.FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker.upload(uf)

    # Add the file picker to the page overlay
    page.overlay.append(file_picker)

    # Add UI elements
    page.add(flt.Column(ref=files))


flt.app(target=myapp)