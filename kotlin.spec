Name:           kotlin
Version:        2.0.21
Release:        1
Summary:        Statically typed programming language

License:        Apache-2.0
URL:            https://kotlinlang.org/
# FIXME we should build this from source instead of using the prebuilt bits
Source0:        https://github.com/JetBrains/kotlin/releases/download/v%{version}/kotlin-compiler-%{version}.zip
Source1:        https://raw.githubusercontent.com/JetBrains/kotlin/v%version/ReadMe.md
BuildArch:      noarch

BuildRequires:  unzip
BuildRequires:  sed
BuildRequires:  bash
BuildRequires:  jre-current
Requires:       jre-current
BuildRequires:  fdupes


%description
Kotlin is a statically typed programming language that targets the JVM,
Android, JavaScript and Native (via kotlin-native). Developed by JetBrains,
the project started in 2010 and had its official 1.0 release in 2016.


%prep
%autosetup -p1 -n kotlinc
sed -i "s|\(DIR *= *\).*|\1%{_bindir}|" bin/*
sed -i "s|\(KOTLIN_HOME *= *\).*|\1%{_datadir}/%{name}|" bin/*

%build

%install
mkdir -p %{buildroot}%{_bindir}/
install -m 0755 bin/kotlin %{buildroot}%{_bindir}/
install -m 0755 bin/kotlin-dce-js %{buildroot}%{_bindir}/
install -m 0755 bin/kotlinc %{buildroot}%{_bindir}/
install -m 0755 bin/kotlinc-js %{buildroot}%{_bindir}/
install -m 0755 bin/kotlinc-jvm %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/%{name}/
install -m 0644 build.txt %{buildroot}%{_datadir}/%{name}/
mkdir -p %{buildroot}%{_datadir}/%{name}/lib/
install -m 0644 lib/* %{buildroot}%{_datadir}/%{name}/lib/
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}/
cd license/ && find * -type f -exec install -Dm 0644 {} %{buildroot}%{_datadir}/licenses/%{name}/{} \;
mkdir -p %{buildroot}%{_docdir}/%{name}
cp %{S:1} %{buildroot}%{_docdir}/%{name}/

%fdupes %buildroot/%_datadir/licenses/%name/


%verifyscript
rm -rf test && mkdir test && cd test
cat <<EOT > test.kt
fun main(args: Array<String>) {
    println("Hello, world!")
}
EOT
kotlinc test.kt && kotlin TestKt
kotlinc test.kt -include-runtime -d test.jar
kotlinc-js test.kt -output test.js
kotlinc-jvm test.kt -include-runtime -d test.jar


%files
%doc %{_docdir}/%{name}
%license %{_datadir}/licenses/kotlin
%{_bindir}/*
%{_datadir}/kotlin
