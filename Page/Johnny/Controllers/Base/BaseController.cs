using Johnny.Models.ViewModel.Base;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Johnny.Controllers.Base
{
    public class BaseController : Controller
    {
         internal BaseViewModel Prepare(BaseViewModel ViewModel,string Titel = null)
        {
            if (ViewModel == null)
                return ViewModel;

            if (!string.IsNullOrEmpty(Titel))
                ViewModel.titel = Titel;
            //Init menu
            ViewModel.Menuitems = new List<Models.Data.Menu>()
            {
                new Models.Data.Menu(){ Link="#",Name="Weather"},
                new Models.Data.Menu(){ Link="#",Name="Who is there?"},
                new Models.Data.Menu(){ Link="#",Name="Configure"}
            };
            return ViewModel;

        }

    }
}
