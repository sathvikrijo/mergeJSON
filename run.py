import json
import os

class MergeJSON(object):
    def __init__(self, path, inPrefix, outPrefix, maxSize):
        self.folderPath = path
        self.inputFile_Prefix, self.outputFile_Prefix = inPrefix, outPrefix
        self.maxFile_Size = maxSize - (0.15 * maxSize)
        self.inputFiles = list()
        self.counter = 1
        self.input_line_no, self.output_line_no = 1, 1
        self.out = None
        self.getInputFiles()
        self.template()
        self.openFile()
        self.parse()

    def getFileSize(self):
        return os.stat(self.outputFile).st_size

    def getInputFiles(self):
        for files in os.listdir(self.folderPath):
            if os.path.isfile(os.path.join(self.folderPath,files)) and self.inputFile_Prefix in files:
                self.inputFiles.append(files)
        self.inputFiles.sort()

    def template(self):
        self.outputFile = self.outputFile_Prefix + str(self.counter) + ".json"
        if(len(self.inputFiles) != 0):
            with open(self.inputFiles[0]) as f:
                self.first_line = f.readline()
                self.end_line = "] }"
        else:
            print("Input files not found")

    def openFile(self):
        self.out = open(self.outputFile,"w")

    def rotateFile(self):
        self.out.seek(-2, os.SEEK_END)
        self.out.truncate()
        self.out.write("\n" + self.end_line)
        self.out.flush()
        self.out.close()
        self.counter += 1
        self.outputFile = self.outputFile_Prefix + str(self.counter) + ".json"
        self.out = open(self.outputFile, "w")
        self.output_line_no = 1
        self.input_line_no += 1


    def parse(self):
        for self.inputFile in self.inputFiles:
            self.input_line_no = 1
            with open(self.inputFile) as self.ins:
                self.data = self.ins.readline()
                while self.data:
                    self.data = self.data.replace("}\n","},\n")
                    if self.output_line_no == 1:
                        self.out.write(self.first_line)
                        self.output_line_no += 1
                    elif self.data == self.end_line or self.input_line_no == 1:
                        pass
                    else:
                        self.out.write(str("\t"+ self.data))
                        self.out.flush()
                    if self.getFileSize() > self.maxFile_Size:
                        self.rotateFile()
                        continue
                    self.data = self.ins.readline()
                    self.input_line_no += 1
            if self.inputFiles.index(self.inputFile) == (len(self.inputFiles)-1):
                self.out.seek(-2, os.SEEK_END)
                self.out.truncate()
                self.out.write("\n" + self.end_line)
                self.out.close()

if __name__ == '__main__':
    path = str(input("Path: "))
    inPrefix = input("Input file prefix: ")
    outPrefix = input("Output file prefix: ")
    maxSize = input("Max File Size allowed (in KB): ")

    mergeJson = MergeJSON(path, inPrefix, outPrefix, maxSize)
    print("Output files generated successfully")
