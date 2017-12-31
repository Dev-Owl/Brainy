
using Microsoft.AspNetCore.Mvc.Rendering;

namespace Johnny.Core.Extension
{
    public static class HtmlHelperExtensions
    {
        public static void AddControl(this IHtmlHelper helper, string ComponentName)
        {
            helper.RenderPartial($"~/Views/Shared/Components/{ComponentName}.html");
        }

        public static void AddControlBundel(this IHtmlHelper helper, string BundleName)
        {
            var bundelService = new ComponentBundels();
            bundelService[BundleName].ForEach(c => helper.RenderPartial(c));
        }
    }
}
