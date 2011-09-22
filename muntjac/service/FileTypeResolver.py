# Copyright (C) 2011 Vaadin Ltd
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.ThemeResource import (ThemeResource,)
# from java.io.File import (File,)
# from java.io.Serializable import (Serializable,)
# from java.util.Collections import (Collections,)
# from java.util.Hashtable import (Hashtable,)
# from java.util.Map import (Map,)
# from java.util.StringTokenizer import (StringTokenizer,)


class FileTypeResolver(Serializable):
    """Utility class that can figure out mime-types and icons related to files.
    <p>
    Note : The icons are associated purely to mime-types, so a file may not have
    a custom icon accessible with this class.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Default icon given if no icon is specified for a mime-type.
    DEFAULT_ICON = ThemeResource('../runo/icons/16/document.png')
    # Default mime-type.
    DEFAULT_MIME_TYPE = 'application/octet-stream'
    # Initial file extension to mime-type mapping.
    _initialExtToMIMEMap = 'application/cu-seeme                            csm cu,' + 'application/dsptype                             tsp,' + 'application/futuresplash                        spl,' + 'application/mac-binhex40                        hqx,' + 'application/msaccess                            mdb,' + 'application/msword                              doc dot,' + 'application/octet-stream                        bin,' + 'application/oda                                 oda,' + 'application/pdf                                 pdf,' + 'application/pgp-signature                       pgp,' + 'application/postscript                          ps ai eps,' + 'application/rtf                                 rtf,' + 'application/vnd.ms-excel                        xls xlb,' + 'application/vnd.ms-powerpoint                   ppt pps pot,' + 'application/vnd.wap.wmlc                        wmlc,' + 'application/vnd.wap.wmlscriptc                  wmlsc,' + 'application/wordperfect5.1                      wp5,' + 'application/zip                                 zip,' + 'application/x-123                               wk,' + 'application/x-bcpio                             bcpio,' + 'application/x-chess-pgn                         pgn,' + 'application/x-cpio                              cpio,' + 'application/x-debian-package                    deb,' + 'application/x-director                          dcr dir dxr,' + 'application/x-dms                               dms,' + 'application/x-dvi                               dvi,' + 'application/x-xfig                              fig,' + 'application/x-font                              pfa pfb gsf pcf pcf.Z,' + 'application/x-gnumeric                          gnumeric,' + 'application/x-gtar                              gtar tgz taz,' + 'application/x-hdf                               hdf,' + 'application/x-httpd-php                         phtml pht php,' + 'application/x-httpd-php3                        php3,' + 'application/x-httpd-php3-source                 phps,' + 'application/x-httpd-php3-preprocessed           php3p,' + 'application/x-httpd-php4                        php4,' + 'application/x-ica                               ica,' + 'application/x-java-archive                      jar,' + 'application/x-java-serialized-object            ser,' + 'application/x-java-vm                           class,' + 'application/x-javascript                        js,' + 'application/x-kchart                            chrt,' + 'application/x-killustrator                      kil,' + 'application/x-kpresenter                        kpr kpt,' + 'application/x-kspread                           ksp,' + 'application/x-kword                             kwd kwt,' + 'application/x-latex                             latex,' + 'application/x-lha                               lha,' + 'application/x-lzh                               lzh,' + 'application/x-lzx                               lzx,' + 'application/x-maker                             frm maker frame fm fb book fbdoc,' + 'application/x-mif                               mif,' + 'application/x-msdos-program                     com exe bat dll,' + 'application/x-msi                               msi,' + 'application/x-netcdf                            nc cdf,' + 'application/x-ns-proxy-autoconfig               pac,' + 'application/x-object                            o,' + 'application/x-ogg                               ogg,' + 'application/x-oz-application                    oza,' + 'application/x-perl                              pl pm,' + 'application/x-pkcs7-crl                         crl,' + 'application/x-redhat-package-manager            rpm,' + 'application/x-shar                              shar,' + 'application/x-shockwave-flash                   swf swfl,' + 'application/x-star-office                       sdd sda,' + 'application/x-stuffit                           sit,' + 'application/x-sv4cpio                           sv4cpio,' + 'application/x-sv4crc                            sv4crc,' + 'application/x-tar                               tar,' + 'application/x-tex-gf                            gf,' + 'application/x-tex-pk                            pk PK,' + 'application/x-texinfo                           texinfo texi,' + 'application/x-trash                             ~ % bak old sik,' + 'application/x-troff                             t tr roff,' + 'application/x-troff-man                         man,' + 'application/x-troff-me                          me,' + 'application/x-troff-ms                          ms,' + 'application/x-ustar                             ustar,' + 'application/x-wais-source                       src,' + 'application/x-wingz                             wz,' + 'application/x-x509-ca-cert                      crt,' + 'audio/basic                                     au snd,' + 'audio/midi                                      mid midi,' + 'audio/mpeg                                      mpga mpega mp2 mp3,' + 'audio/mpegurl                                   m3u,' + 'audio/prs.sid                                   sid,' + 'audio/x-aiff                                    aif aiff aifc,' + 'audio/x-gsm                                     gsm,' + 'audio/x-pn-realaudio                            ra rm ram,' + 'audio/x-scpls                                   pls,' + 'audio/x-wav                                     wav,' + 'image/bitmap                                    bmp,' + 'image/gif                                       gif,' + 'image/ief                                       ief,' + 'image/jpeg                                      jpeg jpg jpe,' + 'image/pcx                                       pcx,' + 'image/png                                       png,' + 'image/svg+xml                                   svg svgz,' + 'image/tiff                                      tiff tif,' + 'image/vnd.wap.wbmp                              wbmp,' + 'image/x-cmu-raster                              ras,' + 'image/x-coreldraw                               cdr,' + 'image/x-coreldrawpattern                        pat,' + 'image/x-coreldrawtemplate                       cdt,' + 'image/x-corelphotopaint                         cpt,' + 'image/x-jng                                     jng,' + 'image/x-portable-anymap                         pnm,' + 'image/x-portable-bitmap                         pbm,' + 'image/x-portable-graymap                        pgm,' + 'image/x-portable-pixmap                         ppm,' + 'image/x-rgb                                     rgb,' + 'image/x-xbitmap                                 xbm,' + 'image/x-xpixmap                                 xpm,' + 'image/x-xwindowdump                             xwd,' + 'text/comma-separated-values                     csv,' + 'text/css                                        css,' + 'text/html                                       htm html xhtml,' + 'text/mathml                                     mml,' + 'text/plain                                      txt text diff,' + 'text/richtext                                   rtx,' + 'text/tab-separated-values                       tsv,' + 'text/vnd.wap.wml                                wml,' + 'text/vnd.wap.wmlscript                          wmls,' + 'text/xml                                        xml,' + 'text/x-c++hdr                                   h++ hpp hxx hh,' + 'text/x-c++src                                   c++ cpp cxx cc,' + 'text/x-chdr                                     h,' + 'text/x-csh                                      csh,' + 'text/x-csrc                                     c,' + 'text/x-java                                     java,' + 'text/x-moc                                      moc,' + 'text/x-pascal                                   p pas,' + 'text/x-setext                                   etx,' + 'text/x-sh                                       sh,' + 'text/x-tcl                                      tcl tk,' + 'text/x-tex                                      tex ltx sty cls,' + 'text/x-vcalendar                                vcs,' + 'text/x-vcard                                    vcf,' + 'video/dl                                        dl,' + 'video/fli                                       fli,' + 'video/gl                                        gl,' + 'video/mpeg                                      mpeg mpg mpe,' + 'video/quicktime                                 qt mov,' + 'video/x-mng                                     mng,' + 'video/x-ms-asf                                  asf asx,' + 'video/x-msvideo                                 avi,' + 'video/x-sgi-movie                               movie,' + 'x-world/x-vrml                                  vrm vrml wrl'
    # File extension to MIME type mapping. All extensions are in lower case.
    _extToMIMEMap = dict()
    # MIME type to Icon mapping.
    _MIMEToIconMap = dict()
    lines = StringTokenizer(_initialExtToMIMEMap, ',')
    while lines.hasMoreTokens():
        line = lines.nextToken()
        exts = StringTokenizer(line)
        type = exts.nextToken()
        while exts.hasMoreTokens():
            ext = exts.nextToken()
            addExtension(ext, type)
    # Initialize Icons
    folder = ThemeResource('../runo/icons/16/folder.png')
    addIcon('inode/drive', folder)
    addIcon('inode/directory', folder)
    # Initialize extension to MIME map

    @classmethod
    def getMIMEType(cls, *args):
        """Gets the mime-type of a file. Currently the mime-type is resolved based
        only on the file name extension.

        @param fileName
                   the name of the file whose mime-type is requested.
        @return mime-type <code>String</code> for the given filename
        ---
        Gets the mime-type for a file. Currently the returned file type is
        resolved by the filename extension only.

        @param file
                   the file whose mime-type is requested.
        @return the files mime-type <code>String</code>
        """
        # Checks for nulls
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], File):
                file, = _0
                if file is None:
                    raise cls.NullPointerException('File can not be null')
                # Directories
                if file.isDirectory():
                    # Drives
                    if file.getParentFile() is None:
                        return 'inode/drive'
                    else:
                        return 'inode/directory'
                # Return type from extension
                return cls.getMIMEType(file.getName())
            else:
                fileName, = _0
                if fileName is None:
                    raise cls.NullPointerException('Filename can not be null')
                # Calculates the extension of the file
                dotIndex = fileName.find('.')
                while dotIndex >= 0 and fileName.find('.', dotIndex + 1) >= 0:
                    dotIndex = fileName.find('.', dotIndex + 1)
                dotIndex += 1
                if len(fileName) > dotIndex:
                    ext = fileName[dotIndex:]
                    # Ignore any query parameters
                    queryStringStart = ext.find('?')
                    if queryStringStart > 0:
                        ext = ext[:queryStringStart]
                    # Return type from extension map, if found
                    type = cls._extToMIMEMap[ext.toLowerCase()]
                    if type is not None:
                        return type
                return cls.DEFAULT_MIME_TYPE
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def getIcon(cls, *args):
        """Gets the descriptive icon representing file, based on the filename. First
        the mime-type for the given filename is resolved, and then the
        corresponding icon is fetched from the internal icon storage. If it is
        not found the default icon is returned.

        @param fileName
                   the name of the file whose icon is requested.
        @return the icon corresponding to the given file
        ---
        Gets the descriptive icon representing a file. First the mime-type for
        the given file name is resolved, and then the corresponding icon is
        fetched from the internal icon storage. If it is not found the default
        icon is returned.

        @param file
                   the file whose icon is requested.
        @return the icon corresponding to the given file
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], File):
                file, = _0
                return cls.getIconByMineType(cls.getMIMEType(file))
            else:
                fileName, = _0
                return cls.getIconByMineType(cls.getMIMEType(fileName))
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def getIconByMineType(cls, mimeType):
        icon = cls._MIMEToIconMap[mimeType]
        if icon is not None:
            return icon
        # If nothing is known about the file-type, general file
        # icon is used
        return cls.DEFAULT_ICON

    # Checks for nulls

    @classmethod
    def addExtension(cls, extension, MIMEType):
        """Adds a mime-type mapping for the given filename extension. If the
        extension is already in the internal mapping it is overwritten.

        @param extension
                   the filename extension to be associated with
                   <code>MIMEType</code>.
        @param MIMEType
                   the new mime-type for <code>extension</code>.
        """
        cls._extToMIMEMap.put(extension.toLowerCase(), MIMEType)

    @classmethod
    def addIcon(cls, MIMEType, icon):
        """Adds a icon for the given mime-type. If the mime-type also has a
        corresponding icon, it is replaced with the new icon.

        @param MIMEType
                   the mime-type whose icon is to be changed.
        @param icon
                   the new icon to be associated with <code>MIMEType</code>.
        """
        cls._MIMEToIconMap.put(MIMEType, icon)

    @classmethod
    def getExtensionToMIMETypeMapping(cls):
        """Gets the internal file extension to mime-type mapping.

        @return unmodifiable map containing the current file extension to
                mime-type mapping
        """
        return Collections.unmodifiableMap(cls._extToMIMEMap)

    @classmethod
    def getMIMETypeToIconMapping(cls):
        """Gets the internal mime-type to icon mapping.

        @return unmodifiable map containing the current mime-type to icon mapping
        """
        return Collections.unmodifiableMap(cls._MIMEToIconMap)