using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Johnny
{
    public class ComponentBundels
    {

        private static Dictionary<string, List<string>> bundels;

        public List<string> this[string Name]
        {
            get{
                if (bundels.ContainsKey(Name))
                    return bundels[Name];
                else
                    throw new KeyNotFoundException($"Unable to find the component bundel named {Name}");
            }
        }

        public ComponentBundels()
        {
        }

        static ComponentBundels()
        {
            bundels = new Dictionary<string, List<string>>();
            CreateBundels();
        }

        private static void CreateBundels()
        {
            bundels.Add("default_controls", new List<string>() {
                "~/Views/Shared/Components/menu.html"
            });
        }



    }
}
