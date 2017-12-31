using Johnny.Models.Data;
using Johnny.Models.ViewModel.Base;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Johnny.Models
{
    public class HomeViewModel : BaseViewModel
    {
        public List<Switch> Switches { get; set; }
    }
}
