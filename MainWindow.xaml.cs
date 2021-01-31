using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using Tesseract;

namespace CopyTranslatePaste
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private async Task<string> Translate(string src)
        {
            return await CopyTranslatePaste.Translate.RunAsync(src);
        }
        
        private void Import_Click(object sender, RoutedEventArgs e)
        {
            var dialog = new OpenFileDialog()
            {
                Filter = "图像文件(.jpg;*.png)|*.jpg;*.png",
                Title = "选取文件"
            };
            if (dialog.ShowDialog().GetValueOrDefault())
            {
                var filePath = dialog.FileName;
                using var ocr = new TesseractEngine(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "tessdata"), "chi_sim", EngineMode.Default);
                var pix = PixConverter.ToPix(new System.Drawing.Bitmap(filePath));
                using var page = ocr.Process(pix);
                string text = page.GetText();
                if (!String.IsNullOrWhiteSpace(text))
                {
                    TextBlockSrc.Text = text.Replace("\n","");
                }
                else
                {
                    TextBlockSrc.Text = "未识别到文字";
                }

            }
        }

        private async void Translate_Click(object sender, RoutedEventArgs e)
        {
            var src = TextBlockSrc.Text;
            if (string.IsNullOrEmpty(src))
            {
                return;
            }
            var result = await Translate(src);
            TextBlockResult.Text = result;

        }
    }
}
