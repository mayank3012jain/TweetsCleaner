#class to clean tweets. It cleans extra white spaces, removes the nmbers in the starting, removes emojis, edits hashtags,
#removes emotions and saves them, replaces name by "*name*" and saves the name
#the class inputs a file to be read, the file to be written on.
import re


class TweetCleaner:

    def __init__(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.inputLine = None
        self.emotion = None
        self.name = None

    def remove_emotion(self):
        emPattern = re.compile(r'::\s\w+')
        emMatch = emPattern.finditer(self.inputLine)
        for match in emMatch:
            # print(match)
            self.emotion = (match.group(0)[3:])
        self.inputLine = emPattern.sub(r'', self.inputLine)

    def remove_name(self):
        namePattern = re.compile(r'@\w+')
        nameMatch = namePattern.finditer(self.inputLine)
        for match in nameMatch:
            self.name = match.group(0)[1:]
        self.inputLine = namePattern.sub(r'*NAME*', self.inputLine)
        # following replaces all the occurances of the name with "*NAME*"
        if self.name:
            namePattern = re.compile(self.name)
            self.inputLine = namePattern.sub("*NAME*", self.inputLine)

    def edit_hashtags(self):
        hash = None
        hashlist = []
        hashPattern = re.compile(r'#\w+')
        hashMatch = hashPattern.finditer(self.inputLine)
        for match in hashMatch:
            hash = match.group(0)[1:]
            # print(hash)
        if hash:
            prev = 0
            for i in range(1, len(hash) - 1):
                if (hash[i].islower() and hash[i + 1].isupper()):
                    hashlist.append(hash[prev:i + 1])
                    prev = i + 1
            hashlist.append(hash[prev:])
            hash = " ".join(hashlist)
            self.inputLine = hashPattern.sub(hash, self.inputLine)

    def remove_spaces(self):
        self.inputLine = " ".join(self.inputLine.split())

    def remove_emojis(self):
        emoPattern = re.compile(r'[():-;\[\]]+')
        self.inputLine = emoPattern.sub("", self.inputLine)

    def clean(self):
        with open(self.inputFile, 'r') as readfile:
            with open(self.outputFile, 'w') as writefile:
                for self.inputLine in readfile:
                    self.inputLine = self.inputLine[20:]  # specifically for the given tweets file
                    self.remove_emotion()
                    self.remove_name()
                    self.edit_hashtags()
                    self.remove_emojis()
                    self.remove_spaces()
                    writefile.write("Tweet: {}\tName: {}\tEmotion: {}\n".format(self.inputLine, self.name, self.emotion))

#following piece of code is only for testing the class.
sample1 = TweetCleaner("tweetsUncleaned.txt", "sampleWriteFile.txt")
sample1.clean()
