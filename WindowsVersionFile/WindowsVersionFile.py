"""
Write a Windows Version file that for example pyinstaller can use to write
version information into the .exe it produces
"""

from time import time

def fill_in_version_file_template(
    filevers = (2, 4, 8, 1),
    prodvers = (2, 4, 0, 0),
    datetime = 0,
    CompanyName = 'Erewhon Inc.',
    FileDescription = 'Erewhon Software Update',
    InternalName = 'Erewhon Software Update',
    LegalCopyright = '(c) 2006-2011, 2015-2017 Erewhon Inc. All rights reserved.',
    OriginalFilename = 'SoftwareUpdate.exe',
    ProductName = 'Erewhon Software Update',
    auto_datetime = False
    ):

    if auto_datetime:
        # Not working
        _secs_since_epoch = time()
        _msd = _secs_since_epoch / 0xFFFFFFFF
        datetime_msd = int(_msd)
        datetime_lsd = int(_secs_since_epoch - datetime_msd * 0xFFFFFFFF)
    else:
        datetime_msd = 0
        datetime_lsd = 0

    FileVersionStr = '{}.{}.{}.{}'.format(*filevers)
    ProductVersionStr = '{}.{}.{}.{}'.format(*prodvers)

    template = f"""
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers={filevers},
    prodvers={prodvers},
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x17,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=({datetime_msd}, {datetime_lsd})
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904b0',
        [StringStruct(u'CompanyName', u'{CompanyName}'),
        StringStruct(u'FileDescription', u'{FileDescription}'),
        StringStruct(u'FileVersion', u'{FileVersionStr}'),
        StringStruct(u'InternalName', u'{InternalName}'),
        StringStruct(u'LegalCopyright', u'{LegalCopyright}'),
        StringStruct(u'OriginalFilename', u'{OriginalFilename}'),
        StringStruct(u'ProductName', u'{ProductName}'),
        StringStruct(u'ProductVersion', u'{ProductVersionStr}')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
    """
    (
    filevers,
    prodvers,
    datetime_msd,
    datetime_lsd,
    CompanyName,
    FileDescription,
    FileVersionStr,
    InternalName,
    LegalCopyright,
    OriginalFilename,
    ProductName,
    ProductVersionStr
    )
    return template

if __name__ == "__main__":
    result = fill_in_version_file_template()
    print(result)

    result2 = fill_in_version_file_template(
    filevers = (0, 1, 1, 0),
    prodvers = (0, 1, 0, 0),
    datetime = 0,
    CompanyName = 'Seven Smiles :)',
    FileDescription = 'WindowsVersionFile',
    InternalName = 'WindowsVersionFile',
    LegalCopyright = '(c) 2019 Tony Whitley. All rights reserved.',
    OriginalFilename = 'WindowsVersionFile.py',
    ProductName = 'WindowsVersionFile'
    )
    print(result2)
