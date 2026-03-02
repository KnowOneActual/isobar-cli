class Isobar < Formula
  include Language::Python::Virtualenv

  desc "Terminal weather tool focused on what it FEELS LIKE outside"
  homepage "https://github.com/KnowOneActual/isobar-cli"
  url "https://files.pythonhosted.org/packages/15/18/06bf59f59c673bd93d747ab73074353d718d52be6a5d695813bbef8f6d26/isobar_cli-1.0.0.tar.gz"
  sha256 "62b28d4f97ae0efced4d18d82e23b636252a9aac74a4a8b2ff8f362c98399f40"
  license "MIT"

  depends_on "python@3.12"

  def install
    # Create a virtualenv in libexec
    venv = virtualenv_create(libexec, "python3.12")
    
    # Install the package and its dependencies from PyPI (using wheels for speed)
    # This is more robust than the previous simple call.
    system libexec/"bin/pip", "install", "isobar-cli"
    
    # Explicitly link the binary so 'isobar' works in the terminal
    bin.install_symlink libexec/"bin/isobar"
  end

  test do
    system "#{bin}/isobar", "--help"
  end
end
