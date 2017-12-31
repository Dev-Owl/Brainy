using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Johnny.Models;
using Johnny.Controllers.Base;

namespace Johnny.Controllers
{
    public class HomeController : BaseController
    {
        public IActionResult Index()
        {
            return View(Prepare( new HomeViewModel() { Switches = new List<Models.Data.Switch>() { new Models.Data.Switch() { Name = "TV", InternalName = "a", Description = "TV und alles was dran hängt", State = false } } },"Home"));
        }

        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
