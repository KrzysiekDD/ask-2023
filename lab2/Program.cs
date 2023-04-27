namespace lab2
{
    internal static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            // To customize application configuration such as set high DPI settings or default font,
            // see https://aka.ms/applicationconfiguration.
            ApplicationConfiguration.Initialize();

            //Form1 form1 = new Form1();
            //Form2 form2 = new Form2();

            //form1.ConnectToForm2(form2);
            //form2.ConnectToForm1(form1);

            Application.Run(new Form1());
        }
    }
}