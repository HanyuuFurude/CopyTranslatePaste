using Microsoft.Win32;
using System;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
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

        private async Task<string> Translate(string src,bool mode = false)
        {
            return await CopyTranslatePaste.Translate.RunAsync(src,mode);
        }

        private async void Import_ClickAsync(object sender, RoutedEventArgs e)
        {
            var dialog = new OpenFileDialog()
            {
                Filter = "图像文件(.jpg;*.png)|*.jpg;*.png",
                Title = "选取文件"
            };
            if (dialog.ShowDialog().GetValueOrDefault())
            {
                TextBlockSrc.Text = " ⏱ OCR执行中...";
                string text;
                var filePath = dialog.FileName;
                try
                {
                    /*
                     * TODO: 做一个映射表，显示用户友好的语言名
                     */
                    var lang = ((ComboBoxItem)ComboBoxLanguageSlected.SelectedItem).Content.ToString();
                    var pix = PixConverter.ToPix(new System.Drawing.Bitmap(filePath));
                    text = await Utils.DoOCR(lang, pix);
                }
                catch (Exception exp)
                {
                    TextBlockSrc.Text = $"{Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "tessdata")}\n{exp.Message}";
                    return;
                }
                if (!String.IsNullOrWhiteSpace(text))
                {
                    if (CheckBoxImportSmartProcess.IsChecked.GetValueOrDefault(true))
                    {
                        text = Utils.TextProcessor(text);
                    }
                    TextBlockSrc.Text = text;
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
            TextBlockResult.Text = " ⏱ 翻译接口请求中...";
            var result = await Translate(src,CheckBoxTranslateResultMode.IsChecked.GetValueOrDefault(false));
            TextBlockResult.Text = result;

        }
    }
}