import re
import os
import glob
import shutil

def _find_ext(filename):
    """
    Finds the LaTeX supported file name corresponding given a LaTeX image filename
    without extension.

    Args:
        filename(str): The name of the image file without extension.

    Return:
        The full filename.
    """
    for ext in [".pdf", ".png", ".jpg", ".eps"]:
        if os.path.exists(filename + ext):
            return ext
    raise Exception("No file with name {} and matching extension found.".format(filename))

class Parser:
    """
    The Parser class takes care of parsing the LaTeX file. During parsing it stores
    all figures included with \includegraphics with their old and new names and
    generates the updates LaTeX document.

    Attributes:
        input(str): The input document as string.
        output(str): The output document with updated references as string.
        files(list): List of pairs (old_file, new_file) of the old and new names of the
            figures found in the document.
    """
    def __init__(self,
                 filename,
                 dest = "figures",
                 filename_template = "fig{:02d}",
                 one_based=True):
        """
        Args:
            filename(str): The filename of the input document.
            dest: Folder to which to copy the renamed figures.
            filename_template: Template for figure names. The final
                filename will be produced using filename_template.format(index), where
                index is the index of the current figure.
            one_based: Whether to start indexing with 0 or 1.
        """
        path = os.path.expandvars(os.path.expanduser(filename))

        with open(path, "rU") as file:
            self.input = file.read()

        self.expr = re.compile(r"(^[^%\n]*)\\includegraphics(:?\[[^\]]*\])?{([^}]*)}", re.MULTILINE)
        self.folder = os.path.dirname(filename)

        self.dest = dest
        self.filename_template = filename_template
        self.one_based = one_based

        self.files = []
        self._parse()

    def _extend_path(self, path):
        if not os.path.isabs(path):
            path = os.path.join(self.folder, path)

        path, ext = os.path.splitext(path)
        if ext == "":
            ext = _find_ext(path)
        path = path + ext
        return path

    def _new_filename(self, old_filename, index):
        old_filename = self._extend_path(old_filename)
        path, name = os.path.split(old_filename)
        name, ext = os.path.splitext(name)

        new_name = self.filename_template.format(index) + ext
        new_filename = os.path.join(self.dest, new_name)
        return new_filename


    def _parse(self):
        if self.one_based:
            index = 1
        else:
            index = 0

        self.output = ""
        current_position = 0

        for match in re.finditer(self.expr, self.input):
            self.output += self.input[current_position : match.start()]
            old_filename = match.group(3)
            new_filename = self._new_filename(old_filename, index)
            repl = r"\1\\includegraphics\2{{{}}}".format(new_filename)
            self.output += match.expand(repl)
            current_position = match.end()

            self.files.append((self._extend_path(old_filename),
                                new_filename))
            index += 1
        self.output += self.input[current_position:]

    def copy_files(self):
        """
        Copy the files found while parsing the LaTeX file to the destination
        folder.
        """
        if not(os.path.exists(self.dest)):
            os.makedirs(self.dest)
        for f1, f2 in self.files:
            if not (f1 == f2):
                shutil.copy(f1, f2)
