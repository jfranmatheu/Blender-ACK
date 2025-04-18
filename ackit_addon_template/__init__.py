# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from .ackit import AddonLoader, AutoCode

def register():
    AddonLoader.init_modules(
        use_autoload=False,
        auto_code={AutoCode.OPS, AutoCode.ICONS, AutoCode.TYPES}
    )
    AddonLoader.register_modules()


def unregister():
    AddonLoader.unregister_modules()
