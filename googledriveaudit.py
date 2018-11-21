#!/usr/bin/env python2.7

import csv
import os
import os.path
import re
from subprocess import call
from subprocess import check_output 
import sys

def createFileList(user):
  gam = "/path/to/gam"
  #gam user $username show filelist allfields > $filename
  output = check_output([gam, "user", user, "show", "filelist", "allfields"])

  #search and replace ^M aka \r\n aka \r
  #not sure why Google Drive allows line breaks in the file name
  output = output.replace('\r', '')

  return saveFile(user.split('@')[0], output, "-allfiles")
  

def saveFile(username, output, filename):
  fileCount = 0
  for file in os.listdir('.'):
    if file.startswith(username + filename):
      fileCount += 1

  if fileCount == 0:
    fileName = username + filename + '.csv'
  else:
    fileName = username + filename + str(fileCount-1) + '.csv'

  file = open(fileName, "w")
  file.write(output)
  file.close()

  return fileName


def lookForSharedFiles(fileName):
  whiteListedDomains = ["yourGoogleAppsDomain.com", "someVendor.com","someContractingCompany.com"]
  whiteListedEmails = ["person@someContractor.com", "person@FriendOfTheCompany.com"]

  fileOutput = "owner,title,id,alternateLink,sharedWith\n"
  fileOutputBatch = ""
  owner = "someone"
  isShared = False

  with open(fileName, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)

    fileCount = 0
    for row in reader:
      fileCount += 1
      people = []
      print "processing " + row['title']

      for k, v in row.items():
        if re.match("permissions\.\d*\.email", k):
          if v != "" and v.lower() not in whiteListedEmails:
            domain = v.split('@')[1]

            if domain not in whiteListedDomains:
              people.append(v)
      if people:
        isShared = True
        fileOutput += row['Owner'] + "," + row['title'] + "," + row['id'] + "," + row['alternateLink'] + "," + " ".join(people) + "\n"
        owner = row['Owner']  #Should put this above the for loop... how?

        for person in people:
          fileOutputBatch += "gam user " + owner + " delete drivefileacl " + row['id'] + " " + person + "\n"
          fileOutputBatch += "commit-batch\n"


    saveFile(owner, fileOutput, "-logfile")

    file = open(owner+"-batch.gam", "w")
    file.write(fileOutputBatch)
    file.close()

    if not isShared:
      print "No files shared with outsiders."
    print "file count is " + str(fileCount)


#assuming valid user
user = sys.argv[1]
lookForSharedFiles(createFileList(user))