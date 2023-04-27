namespace lab2
{
    partial class Form2
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            richTextBox2 = new RichTextBox();
            textInput2 = new TextBox();
            label1 = new Label();
            button1 = new Button();
            button2 = new Button();
            textBox1 = new TextBox();
            SuspendLayout();
            // 
            // richTextBox2
            // 
            richTextBox2.Location = new Point(29, 48);
            richTextBox2.Name = "richTextBox2";
            richTextBox2.ReadOnly = true;
            richTextBox2.Size = new Size(294, 323);
            richTextBox2.TabIndex = 4;
            richTextBox2.Text = "";
            // 
            // textInput2
            // 
            textInput2.Location = new Point(363, 48);
            textInput2.Multiline = true;
            textInput2.Name = "textInput2";
            textInput2.Size = new Size(300, 323);
            textInput2.TabIndex = 5;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(325, 30);
            label1.Name = "label1";
            label1.Size = new Size(39, 15);
            label1.TabIndex = 6;
            label1.Text = "User 2";
            label1.Click += label1_Click;
            // 
            // button1
            // 
            button1.Location = new Point(216, 398);
            button1.Name = "button1";
            button1.Size = new Size(249, 74);
            button1.TabIndex = 7;
            button1.Text = "Send to window 1";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // button2
            // 
            button2.Location = new Point(524, 433);
            button2.Name = "button2";
            button2.Size = new Size(139, 39);
            button2.TabIndex = 8;
            button2.Text = "Add word to banned list";
            button2.UseVisualStyleBackColor = true;
            button2.Click += button2_Click;
            // 
            // textBox1
            // 
            textBox1.Location = new Point(524, 398);
            textBox1.Name = "textBox1";
            textBox1.Size = new Size(139, 23);
            textBox1.TabIndex = 9;
            // 
            // Form2
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.Cyan;
            ClientSize = new Size(684, 511);
            Controls.Add(textBox1);
            Controls.Add(button2);
            Controls.Add(button1);
            Controls.Add(label1);
            Controls.Add(textInput2);
            Controls.Add(richTextBox2);
            Name = "Form2";
            Text = "Form2";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private RichTextBox richTextBox2;
        private TextBox textInput2;
        private Label label1;
        private Button button1;
        private Button button2;
        private TextBox textBox1;
    }
}