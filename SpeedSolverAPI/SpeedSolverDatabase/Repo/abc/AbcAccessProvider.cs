﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SpeedSolverDatabase.Repo.abc
{
    public abstract class AbcAccessProvider
    {

        public readonly SpeedContext _context = new SpeedContext();

    }
}