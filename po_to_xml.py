# -*- coding: utf-8 -*-

import codecs, re, os, sys, traceback

#headers
#xml file
xml_header = u"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\r\n"
xml_project = u"<!--Project: %s -->\r\n"
xml_date = u"<!-- translation date: %s -->\r\n"
xml_translator = u"<!-- translator: %s -->\r\n"
xml_opentab = u"<strings>\r\n"
xml_closetab = u"</strings>\r\n"
xml_stringline = u'''  <string id="%s">%s</string>\r\n'''

#po file
po_project = '''"Project-Id-Version: (.*?)\\\\n"'''
po_date = '''"PO-Revision-Date: (.*?)\\\\n"'''
po_translator = '''"Last-Translator: (.*?) <(.*?)>\\\\n"'''
po_language = '''"Language: (.*?)\\\\n"'''
po_string_id = '''msgctxt "#(.*?)"'''
po_string = '''msgstr "(.*?)"'''

class Converter():
    def __init__( self ):
        try:
            success = self.read_po_file( sys.argv[1] )
            if not success:
                print "error in conversion"
            else:
                print "Finished converting .po files"
        except:
            traceback.print_exc()
            print "please use proper starting method"

    def read_po_file( self, root_filepath ):
        language_paths = []
        root_language_path = ""
        addon = os.path.basename( root_filepath )
        # check for type of addon as the language files are stored in different paths
        if addon.split(".")[0] in ( "plugin", "script", "metadata", "visualization", "screensaver" ):
            root_language_path = os.path.join( root_filepath, "resources", "language" ).replace( "\\\\", "\\" )
        elif addon.split(".")[0] in ( "skin" ):
            root_language_path = os.path.join( root_filepath, "language" ).replace( "\\\\", "\\" )
        # get the directory list of language path
        if not root_language_path:
            print "No Root directory found for Language path"
            return False # something wrong with the addon path
        languages = os.listdir( root_language_path )
        if not languages:
            print "Nothing found in language path"
            return False # nothing found in the language folder
        for language in languages:
            # if the path is a folder, join 'string.po' to the end of the path and store for later
            if language:
                _path = os.path.join( root_language_path, language, "strings.po" ).replace( "\\\\", "\\" )
                language_paths.append( _path )
            else:
                continue
        if not language_paths:
            print "No Folders found in Language path"
            return False # no folders found in language path
        for language_path in language_paths:
            if not os.path.exists( language_path ):
                continue
            try:
                po_file = codecs.open( language_path, "r", "utf-8" ).readlines()
                _strings = []
                translator = ""
                translate_date = ""
                project = ""
                for i in range( len( po_file ) ):
                    _string = {}
                    s = ""
                    s_id = ""
                    if not translator:
                        translator_match = re.search( po_translator, po_file[i] )
                        if translator_match:
                            translator = translator_match.group(1)
                    if not translate_date:
                        translate_date_match = re.search( po_date, po_file[i] )
                        if translate_date_match:
                            translate_date = translate_date_match.group(1)
                    if not project:
                        project_match = re.search( po_project, po_file[i] )
                        if project_match:
                            project = project_match.group(1)
                    match = re.search( po_string_id, po_file[i] )
                    if match:
                        s_id = match.group(1)
                        match2 = re.search( po_string, po_file[i + 2] )
                        if match2:
                            s = match2.group(1)
                        _string["id"] = s_id
                        _string["text"] = s
                        _strings.append( _string )
                        i=+2
            except Exception, e:
                traceback.print_exc()
                print e
                continue
            try:
                xml_file_path = os.path.join( os.path.dirname( language_path ), "string.xml" ).replace( "\\\\", "\\" )
                xml_file = codecs.open( xml_file_path, "w", "utf-8" )
                xml_file.write( xml_header )
                xml_file.write( ( xml_project % project ) )
                xml_file.write( ( xml_date % translate_date ) )
                xml_file.write( ( xml_translator % translator ) )
                xml_file.write( xml_opentab )
                for xml_string in _strings:
                    xml_file.write( ( xml_stringline % ( xml_string["id"], xml_string["text"] ) ) )
                xml_file.write( xml_closetab )
                xml_file.close()
                #return True
            except Exception, e:
                print "Problem saving file"
                traceback.print_exc()
                print e
        return True

if ( __name__ == "__main__" ):
    # start
    Converter()