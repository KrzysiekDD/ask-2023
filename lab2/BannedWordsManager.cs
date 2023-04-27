using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Collections.Generic;

namespace lab2
{
    using System.IO;
    using System.Collections.Generic;

    public class BannedWordsManager
    {
        private List<string> _bannedWords = new List<string>();
        private string _filePath;

        public BannedWordsManager(string filePath)
        {
            _filePath = filePath;
            LoadBannedWords();
        }

        private void LoadBannedWords()
        {
            if (File.Exists(_filePath))
            {
                _bannedWords = new List<string>(File.ReadAllLines(_filePath));
            }
        }

        public bool ContainsBannedWords(string inputText)
        {
            foreach (string word in _bannedWords)
            {
                if (inputText.Contains(word))
                {
                    return true;
                }
            }

            return false;
        }

        public void AddBannedWord(string word)
        {
            _bannedWords.Add(word);
            File.AppendAllLines(_filePath, new[] { word });
        }
    }
}
