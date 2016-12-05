import subprocess
import yaml
from github import Github
import os
import urlparse
import urllib


GIT_USERNAME = os.environ['GIT_USERNAME']
GIT_PASSWORD = os.environ['GIT_PASSWORD']

g = Github(GIT_USERNAME, GIT_PASSWORD)

f = open('template.yml')
# use safe_load instead load
dataMap = yaml.safe_load(f)
f.close()

technical_items = {}
main_items = {}

# dataMap['menu']['items']['technical'] = technical_items
dataMap['menu']['items'] = main_items

class docsgen():
    def __init__(self):
        self._prep_dirs()
        self._prep_core_index_file()
        self._prep_general_index_file()
        self._get_repos()
        self._create_index()
        self._create_core_index()
        self._add_core_index_to_dataMap()
        self._output_yaml()
        pass

    def _prep_dirs(self):
        try:
            os.mkdir('techdocs')
            os.removedirs('docs')
            os.mkdir('docs')
        except OSError:
            pass

    def _get_repos(self):
        # From githubpython
        for repo in g.get_user().get_repos():
            if "pearsontechnology" in repo.ssh_url:
                self._get_docs(name=repo.name, url=repo.clone_url, directory="./techdocs/")

    def _create_core_index(self):
        content_path = 'techdocs'
        index_file = '{0}/coreindex.md'.format(content_path)
        for line in os.listdir(content_path):
            if os.path.isdir(os.path.join(content_path, line)):
                doc = "[{0}]({0}/readme.html)".format(line)
                f1=open(index_file, 'a')
                f1.write(doc)
                f1.write("\n")
                f1.write("\n")

    def _create_index(self):
        content_path = 'content'
        blacklist = ['images', 'attachments', 'archive', 'delete']
        for listname in os.listdir(content_path):
            if listname in blacklist:
                continue
            filepath = os.path.join(content_path, listname)
            if os.path.isdir(filepath):
                print "Adding readme link to {0}".format(listname)
                docname = str(listname).replace("-", " ").title()
                doc = "[{0}](/{0}/readme.html)".format(listname)
                main_items[listname] = {
                    'text': docname,
                    'relativeUrl': '/{0}/readme.html'.format(listname)
                }

            if os.path.isfile(filepath):
                if not self.is_markdown(listname):
                    print "Not a markdown: {0}".format(listname)
                    continue
                print "Adding {0} to index".format(listname)
                docname = str(listname).replace(".md", ".html").lower()
                pagename = str(listname).replace(".md", "").title()
                doc = "[{0}](/{1})".format(pagename, docname)
                f1=open('techdocs/index.md', 'a')
                f1.write(doc)
                f1.write("\n")
                f1.write("\n")

    def is_markdown(self, filename):
        return filename.endswith(".md")

    def _add_core_index_to_dataMap(self):
        technical_items['repository-index'] = {
            'text': 'Repository Index',
            'relativeUrl': 'coreindex.html'
        }
        main_items['document-index'] = {
            'text': 'Document Index',
            'relativeUrl': 'index.html'
        }

    def _prep_core_index_file(self):
        f1=open('techdocs/coreindex.md', 'w')
        f1.write("## Index of Repositories / Documents \n \
- - - \n \
\n")

    def _prep_general_index_file(self):
        f1=open('techdocs/index.md', 'w')
        f1.write("## Index of Documents \n \
- - - \n \
\n")

    def _get_docs(self, name, url, directory):
        auth_url = self.get_auth_url(url)
        try:
            command = "git clone " + auth_url
            result = self._cmd_exec(command=command, directory=directory)
            print "git clone result: {0}".format(result)
            # if "fatal" in result:
            #    command = "git pull"
            #   result = self._cmd_exec(command=command, directory="./techdocs/" + name)
        except Exception as e:
            print "git {0} got exception: {1}".format(auth_url, e)

    def get_auth_url(self, url):
        parts = urlparse.urlparse(url)
        netloc = parts.netloc
        encoded_username = urllib.quote(GIT_USERNAME)
        encoded_password = urllib.quote(GIT_PASSWORD)
        location_with_password = '{0}:{1}@{2}'.format(encoded_username, encoded_password, netloc)
        parts = parts._replace(netloc=location_with_password)
        return parts.geturl()

    def _cmd_exec(self, command, directory):
        p = subprocess.Popen(command, shell=True, cwd=directory, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        out, err = p.communicate('foo\nfoofoo\n')
        return err

    def _output_yaml(self):
        with open('couscous.yml', 'w') as f:
            yaml.safe_dump(dataMap, f, default_flow_style=False, indent=4)

docsgen()
