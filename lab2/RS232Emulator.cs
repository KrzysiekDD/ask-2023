using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace lab2
{
    public class RS232Emulator
    {
        public event EventHandler<string> BinaryDataSent;
        public event EventHandler<string> AsciiDataReceived;

        public string SendData(string data)
        {
            StringBuilder encodedData = new StringBuilder();

            data += "\n";

            foreach (char c in data)
            {
                string binaryString = Convert.ToString(c, 2).PadLeft(8, '0');
                encodedData.Append("0" + binaryString + "11");
            }

            BinaryDataSent?.Invoke(this, encodedData.ToString());
            AsciiDataReceived?.Invoke(this, data);
            return encodedData.ToString();
        }
    }
    //public class RS232Emulator
    //{
    //    public delegate void DataReceivedEventHandler(object sender, string data);
    //    public event DataReceivedEventHandler DataReceived;

    //    public string SendData(string data)
    //    {
    //        StringBuilder encodedData = new StringBuilder();
    //        foreach (char c in data)
    //        {
    //            string binaryString = Convert.ToString(c, 2).PadLeft(8, '0');
    //            encodedData.Append("0" + binaryString + "11");
    //        }

    //        DataReceived?.Invoke(this, encodedData.ToString());
    //        return encodedData.ToString();
    //    }

    //    //public void SendData(string data)
    //    //{
    //    //    byte[] asciiBytes = Encoding.ASCII.GetBytes(data);

    //    //    StringBuilder encodedMessage = new StringBuilder();

    //    //    // Iterate through the byte array
    //    //    foreach (byte asciiByte in asciiBytes)
    //    //    {
    //    //        string binaryRepresentation = Convert.ToString(asciiByte, 2).PadLeft(8, '0');


    //    //        encodedMessage.Append('0');
    //    //        encodedMessage.Append(binaryRepresentation);
    //    //        encodedMessage.Append("11");
    //    //        //string encodedByte = "0" + binaryRepresentation + "11";

    //    //        //encodedMessage.Append(encodedByte);
    //    //    }


    //    //    DataReceived?.Invoke(this, encodedMessage.ToString());
    //    //}

    //    public void ReceiveData(string encodedData)
    //    {
    //        List<byte> decodedBytes = new List<byte>();

    //        for (int i = 0; i + 10 < encodedData.Length; i+= 11)
    //        {
    //            // Extract the encoded byte first
    //            //int length = (i + 11 <= encodedData.Length) ? 11 : encodedData.Length - 1;
    //            //string encodedByte = encodedData.Substring(i, length);
    //            string encodedByte = encodedData.Substring(i, 11);

    //            // When the start and two stop bits are removed decode the data to ASCII
    //            string binaryString = encodedByte.Substring(1, 8);

    //            byte asciiValue = Convert.ToByte(binaryString, 2);

    //            decodedBytes.Add(asciiValue);
    //        }

    //        string decodedText = Encoding.ASCII.GetString(decodedBytes.ToArray());

    //        DataReceived?.Invoke(this, decodedText);
    //    }

    //}
}
