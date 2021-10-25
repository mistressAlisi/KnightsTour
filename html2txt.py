#!/usr/bin/python3
import sys,getopt,urllib.request,re,string,argparse
from bs4 import BeautifulSoup

def main(argv):
   # Step One: Validate our Input. We need two variables we'll get with argparse: Input File (or URI), and Output file location:
   parser = argparse.ArgumentParser(description='Strip the HTML tags, and convert remaining text to space separated word lists for any given HTML URL.')
   parser.add_argument('url', metavar='u', type=str, nargs='+',
                    help='URL of location to access for content (the page to convert).')
   parser.add_argument('file', metavar='f', type=str, nargs='+',
                    help='The name of the file to write the results of the conversion to.')
   
   args = parser.parse_args()
   print ("HTML2Txt Scraper...")
   print ('Input URL is \'{}\''.format(args.url[0]))
   print ('Output file is \'{}\''.format(args.file[0]))
   # Get remote HTTP data with urllib.request:
   html_data = urllib.request.urlopen(args.url[0]).read().decode("utf-8")
   # Then use regular expressions to clean it up:
   # First step first; Clean and remove HTML tags with BeautifulSoup:
   soup = BeautifulSoup(html_data,'lxml')
   text_data = soup.get_text()
   
   # Protip: remove line return first, and replace it for a punctuation so it will be cleaned up later, without words getting mangled up:
   punct = re.compile('\n')
   text_data = punct.sub('.', text_data)
   # Now, clean up the remaining string data:
   # we edited string.punctuation to take out the apostrophe ('): That really wrecks the bard: Instead we just delete the apos:
   punct = re.compile('[%s]' % re.escape('!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'))
   text_data = punct.sub(' ', text_data)
   punct = re.compile('[%s]' % re.escape('\''))
   text_data = punct.sub('', text_data)
   # finally, we have some extraneous spaces we can remove:
   punct = re.compile('[\s]{2,}')
   text_data = punct.sub(' ', text_data)
   # finally, let's save data to the specified path:
   output = open(args.file[0],"w+")
   output.write(text_data+" ")
   output.close()
   # And we're all done!
   print ("HTML2Txt Scraper complete")
   
# Finally, we call our main() function when the script is called from the shell:
if __name__ == "__main__":
   main(sys.argv[1:])
