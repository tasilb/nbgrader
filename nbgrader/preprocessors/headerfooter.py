from IPython.nbconvert.preprocessors import Preprocessor
from IPython.nbformat.current import read as read_nb
from IPython.utils.traitlets import Unicode


class IncludeHeaderFooter(Preprocessor):
    """A preprocessor for adding header and/or footer cells to a notebook."""

    header = Unicode("", config=True, help="Path to header notebook")
    footer = Unicode("", config=True, help="Path to footer notebook")

    def preprocess(self, nb, resources):
        """Concatenates the cells from the header and footer notebooks to the
        given cells.

        """
        new_cells = []

        # header
        if self.header:
            with open(self.header, 'r') as fh:
                header_nb = read_nb(fh, 'ipynb')
            new_cells.extend(header_nb.worksheets[0].cells)

        # body
        new_cells.extend(nb.worksheets[0].cells)

        # footer
        if self.footer:
            with open(self.footer, 'r') as fh:
                footer_nb = read_nb(fh, 'ipynb')
            new_cells.extend(footer_nb.worksheets[0].cells)

        nb.worksheets[0].cells = new_cells
        super(IncludeHeaderFooter, self).preprocess(nb, resources)

        return nb, resources

    def preprocess_cell(self, cell, resources, cell_index):
        return cell, resources
