using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO.Ports;
using System.Windows.Forms;

namespace lab2
{
    public partial class Form2 : Form
    {
        private RS232Emulator _rs232Emulator1;
        private RS232Emulator _rs232Emulator2;
        private BannedWordsManager _bannedWordsManager;


        public Form2()
        {
            _rs232Emulator2 = new RS232Emulator();
            _rs232Emulator2.AsciiDataReceived += _rs232Emulator2_DataReceived;

            string filePath = "banned_words.txt";
            _bannedWordsManager = new BannedWordsManager(filePath);

            InitializeComponent();
        }
        public void ConnectToForm1(Form1 form1)
        {
            _rs232Emulator2.AsciiDataReceived += form1._rs232Emulator1_DataReceived;
        }

        public void _rs232Emulator2_DataReceived(object sender, string data)
        {
            Invoke(new Action(() => richTextBox2.AppendText(data)));
        }

        public bool ContainsDisallowedWords(string inputText, string[] disallowedWords)
        {
            foreach (string word in disallowedWords)
            {
                if (inputText.Contains(word))
                {
                    return true;
                }
            }

            return false;
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            //string binaryData = _rs232Emulator1.SendData(textInput1.Text);
            //richTextBox1.AppendText(binaryData);
            //string[] disallowedWords = { "dupa", "kupa", "morderca" }; // Replace with your list of disallowed words

            if (_bannedWordsManager.ContainsBannedWords(textInput2.Text))
            {
                MessageBox.Show("Your message contains banned words. Please remove them before sending them to the other user.");
            }
            else
            {
                _rs232Emulator2.SendData(textInput2.Text);
                textInput2.Clear();
            }
            //_rs232Emulator1.SendData(textInput1.Text);
            //textInput1.Clear();
            //richTextBox1.Clear();

        }

        private void button2_Click(object sender, EventArgs e)
        {
            string newWord = textBox1.Text;
            _bannedWordsManager.AddBannedWord(newWord);
            textBox1.Clear();
        }
    }
}
