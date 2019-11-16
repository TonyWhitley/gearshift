
from WindowsVersionFile.WindowsVersionFile import fill_in_version_file_template

result = fill_in_version_file_template(
  filevers = (3, 1, 58, 0),
  prodvers = (3, 1, 0, 0),
  datetime = 0,
  CompanyName = 'Seven Smiles :)',
  FileDescription = 'rFactor 2 Realistic Gearshift',
  InternalName = 'rFactor 2 Realistic Gearshift',
  LegalCopyright = '(c) 2019 Tony Whitley. All rights reserved.',
  OriginalFilename = 'Gearshift.exe',
  ProductName = 'Gearshift'
  )
print(result)