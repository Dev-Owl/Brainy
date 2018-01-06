using Johnny.Models.Data;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Johnny.Models.ViewModel.Base
{
    public class BaseViewModel
    {
        public string titel { get; set; }
        public List<Menu> Menuitems { get; set; }
    }
}
