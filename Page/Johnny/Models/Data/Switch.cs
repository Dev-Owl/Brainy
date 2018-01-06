using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using PillowSharp.CouchType;

namespace Johnny.Models.Data
{
    public class Switch : CouchDocument
    {
        public string InternalName { get; set; }
        public string Name { get; set; }
        public bool State { get; set; }
        public string Description { get; set; }
    }
}
