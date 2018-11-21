# googledriveaudit
this is a quick wrapper around gam to audit your organization's google drive and look for files that are shared outside your company's domain. this is really slow, but it does the job and i'm not spending money on 3rd party tools that charge per user.

assumes:
- gam is setup 
- you have full access your organization's google apps

usage: <code>./googledriveaudit.py \<userEmailAddress\></code>

if there's any files shared with outsiders, a batch file will be created to remove access.
look through the batch file and remove the entries for those who still need file access.

to execute a gam batch file: <code>gam batch \<batch-filename\></code>
