using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace CopyTranslatePaste
{
    public class Translate
    {
        private const string _RAW_URL = "aHR0cDovL2ZhbnlpLnlvdWRhby5jb20vdHJhbnNsYXRlP3NtYXJ0cmVzdWx0PWRpY3Qmc21hcnRyZXN1bHQ9cnVsZSZzbWFydHJlc3VsdD11Z2Mmc2Vzc2lvbkZyb209bnVsbA==";
        private static readonly string _URL = Utils.Base64Decode(_RAW_URL);
        private static readonly HttpClient _client = new HttpClient();
        private static readonly Dictionary<string, string> _HEADER = new Dictionary<string, string>()
        {
            {"type","AUTO" },
            {"doctype","json" },
            {"version","2.1" },
            {"ue","UTF-8" },
            {"action","FY_BY_CLICKBUTTON" },
            {"typoResult","true" }
        };
        public static async Task<string> RunAsync(string src)
        {
            if (string.IsNullOrWhiteSpace(src))
            {
                return "";
            }
            HttpResponseMessage request = new HttpResponseMessage();
            foreach (var pair in _HEADER)
            {
                request.Headers.Add(pair.Key, pair.Value);
            }
            request.Headers.Add("i", src);
            try
            {
                var response = await _client.GetAsync(_URL);
                response.EnsureSuccessStatusCode();
                var rawRes = await response.Content.ReadAsStringAsync();
                return rawRes;
            }
            catch (Exception e)
            {
                return $"出现错误\n{e.Message}\n{e.StackTrace}";
            }
        }
    }
}
