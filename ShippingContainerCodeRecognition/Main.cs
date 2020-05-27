using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Emgu.CV;
using Emgu.CV.Structure;
using Emgu.CV.Util;
using Emgu.CV.OCR;
using System.Reflection;
using System.IO;

namespace ShippingContainerCodeRecognition
{
    public partial class Main : Form
    {
        Image<Bgr, byte> mImgInput;
        public Main()
        {
            InitializeComponent();
        }

        private void cZoom_CheckedChanged(object sender, EventArgs e)
        {
            
        }

        private void Main_Load(object sender, EventArgs e)
        {

        }

        private void btBrowser_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog ofd = new OpenFileDialog())
            {
                ofd.Filter = "Image file | *.png;*.jpg;*.bmp;*.jpeg;*.tiff";
                if(ofd.ShowDialog() == DialogResult.OK)
                {
                    if(mImgInput != null)
                    {
                        mImgInput.Dispose();
                        mImgInput = null;
                    }
                    mImgInput = new Image<Bgr, byte>(ofd.FileName);
                    string path = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) + "\\";
                    Console.WriteLine(path);
                    var _ocr = new Tesseract(path, "eng", OcrEngineMode.Default);
                    _ocr.SetImage(mImgInput);
                    _ocr.Recognize();
                    var result = _ocr.GetCharacters();
                    string str = string.Empty;
                    for (int i = 0; i < result.Length; i++)
                    {
                        char ct = result[i].Text[0];
                        int val = (int)ct;
                        if ((val >=0x30 && val <= 0x39) || (val >= 0x41 && val <= 0x5a) || (val >= 0x61 && val <= 0x7a))
                        {
                            str += result[i].Text;
                        }
                        
                    }
                    Console.WriteLine(str);
                }
            }
        }
        private void Read(Image<Bgr, byte> ImgSource)
        {

        }


    }
}
