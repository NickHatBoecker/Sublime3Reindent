import sublime
import sublime_plugin
import re

class NhbReindentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("Preferences.sublime-settings")
        tabSize = settings.get("tab_size", 1)

        # determine wrong tab size, which we will replace
        oldTabSize = 2
        if tabSize == 2:
            oldTabSize = 4

        view = self.view
        selection = view.sel()
        lineNums = [view.rowcol(line.a)[0] for line in view.lines(selection[0])]

        for row in lineNums:
            pt = view.text_point(row, 0)
            line = view.line(pt)

            string = self.view.substr(line)
            strippedString = string.lstrip()

            if len(strippedString) > 0:
                whitespaces = re.match("^(\s{1,})[^\s].*", string)

                oldIndent = 0
                if whitespaces:
                    oldIndent = int(len(whitespaces.group(1))/oldTabSize)

                # Remove line
                self.view.erase(edit, sublime.Region(pt + len(string),pt))

                # Write new line
                newWhitespaces = ' '*oldIndent*tabSize
                self.view.insert(edit, pt, newWhitespaces + strippedString)
