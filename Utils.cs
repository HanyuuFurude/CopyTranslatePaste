using System;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Tesseract;

namespace CopyTranslatePaste
{
    class Utils
    {
        public static string Base64Code(string Message)
        {
            byte[] bytes = Encoding.Default.GetBytes(Message);
            return Convert.ToBase64String(bytes);
        }

        public static string Base64Decode(string Message)
        {
            byte[] bytes = Convert.FromBase64String(Message);
            return Encoding.Default.GetString(bytes);
        }

        public static string TextProcessor(string src)
        {
            var res = src;
            // 连字符单词合并
            res = Regex.Replace(res, "([^\n])-\n([^\n])", "$1$2");
            // 文本断行合并
            res = Regex.Replace(res, "([^\n])\n([^\n])", "$1 $2");
            // 多个换行合并成一行
            res = Regex.Replace(res, "\n+", "\n");
            return res;
        }
        public async static Task<string> DoOCR(string lang,Pix pix)
        {
            var task = Task.Run(() =>
            {
                using var ocr = new TesseractEngine(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "tessdata"), lang, EngineMode.Default);
                using var page = ocr.Process(pix);
                return page.GetText();
            });
            return await task;
        }
    }
}
