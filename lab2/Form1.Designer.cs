namespace lab2
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            button1 = new Button();
            label1 = new Label();
            richTextBox1 = new RichTextBox();
            textInput1 = new TextBox();
            button2 = new Button();
            textBox1 = new TextBox();
            SuspendLayout();
            // 
            // button1
            // 
            button1.Location = new Point(215, 398);
            button1.Name = "button1";
            button1.Size = new Size(249, 74);
            button1.TabIndex = 0;
            button1.Text = "Send to window 2";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(327, 28);
            label1.Name = "label1";
            label1.Size = new Size(39, 15);
            label1.TabIndex = 2;
            label1.Text = "User 1";
            label1.Click += label1_Click;
            // 
            // richTextBox1
            // 
            richTextBox1.Location = new Point(366, 47);
            richTextBox1.Name = "richTextBox1";
            richTextBox1.ReadOnly = true;
            richTextBox1.Size = new Size(294, 323);
            richTextBox1.TabIndex = 3;
            richTextBox1.Text = "";
            // 
            // textInput1
            // 
            textInput1.Location = new Point(25, 47);
            textInput1.Multiline = true;
            textInput1.Name = "textInput1";
            textInput1.Size = new Size(300, 323);
            textInput1.TabIndex = 6;
            // 
            // button2
            // 
            button2.Location = new Point(521, 433);
            button2.Name = "button2";
            button2.Size = new Size(139, 39);
            button2.TabIndex = 7;
            button2.Text = "Add word to banned list";
            button2.UseVisualStyleBackColor = true;
            button2.Click += button2_Click;
            // 
            // textBox1
            // 
            textBox1.Location = new Point(521, 398);
            textBox1.Name = "textBox1";
            textBox1.Size = new Size(139, 23);
            textBox1.TabIndex = 8;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.Lime;
            ClientSize = new Size(684, 511);
            Controls.Add(textBox1);
            Controls.Add(button2);
            Controls.Add(textInput1);
            Controls.Add(richTextBox1);
            Controls.Add(label1);
            Controls.Add(button1);
            Name = "Form1";
            Text = "Form1";
            Load += Form1_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button button1;
        private Label label1;
        private RichTextBox richTextBox1;
        private TextBox textInput1;
        private Button button2;
        private TextBox textBox1;
    }
}