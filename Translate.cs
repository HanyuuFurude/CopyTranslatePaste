using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace CopyTranslatePaste
{
    public class Translate
    {
        private const string _RAW_URL = "aHR0cDovL2ZhbnlpLnlvdWRhby5jb20vdHJhbnNsYXRl";
        private const string _USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56";
        private static readonly string _URL = Utils.Base64Decode(_RAW_URL);
        //private static readonly string _URL = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null&i=word&doctype=json";
        private static readonly HttpClient _client = new HttpClient();
        private static readonly Dictionary<string, string> _HEADER = new Dictionary<string, string>()
        {
            {"type","AUTO" },
            {"doctype","json" },
            {"version","2.1" },
            {"ue","UTF-8" },
            {"action","FY_BY_CLICKBUTTON" },
            {"typoResult","true" },
            {"i","测试" }
        };
        public static async Task<string> RunAsync(string src)
        {
            if (string.IsNullOrWhiteSpace(src))
            {
                return "";
            }
            var request = new HttpRequestMessage()
            {
                Method = HttpMethod.Post,
                RequestUri = new Uri(_URL)
            };
            request.Headers.Add("user-agent", _USER_AGENT);
            var content = new Dictionary<string, string>(_HEADER);
            content["i"] = src;
            request.Content = new FormUrlEncodedContent(content);
            try
            {
                var response = await _client.SendAsync(request);
                response.EnsureSuccessStatusCode();
                var rawRes = await response.Content.ReadAsByteArrayAsync();
                var text = Encoding.Default.GetString(rawRes);

                var jobj = JObject.Parse(text);
                var resList = jobj["translateResult"].Value<JArray>();
                StringBuilder result = new StringBuilder();
                foreach(var subResList in resList.Children())
                {
                    foreach(var i in subResList.Children())
                    result.Append(i["tgt"].Value<string>());
                }
                return result.ToString();
            }
            catch (Exception e)
            {
                return $"出现错误\n{e.Message}\n{e.StackTrace}";
            }
        }

    }
}
