# Maintainer: Senin Adin <mail@example.com>
pkgname=archnova
pkgver=1.0.0
pkgrel=1
pkgdesc="Gradient'li, canli, goz alici sistem bilgisi araci"
arch=('any')
url="https://github.com/KULLANICI/archnova"
license=('MIT')
depends=('python')
optdepends=('pciutils: GPU bilgisi' 'ttf-jetbrains-mono-nerd: ikonlar')
makedepends=('python-build' 'python-installer' 'python-setuptools' 'python-wheel')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
  cd "$pkgname-$pkgver"
  python -m build --wheel --no-isolation
}

package() {
  cd "$pkgname-$pkgver"
  python -m installer --destdir="$pkgdir" dist/*.whl
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
