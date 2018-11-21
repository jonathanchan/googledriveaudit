# googledriveaudit
audit google drive files shared outside your company's domain

assumes:
- gam is setup 
- you have full access your company's to google apps

usage: <code>./googledriveaudit.py \<userEmailAddress\><code>

if there's any files shared with outsiders, a batch file will be created to remove access.
look through the batch file and remove the entries for those who still need file access.

to execute a gam batch file: <code>gam batch \<batch-filename\></code>
