#!/bin/bash

PKG_FULL_HOME_PATH="${PREFIX}/share/${PKG_NAME}"
PKG_FULL_HOME_PATH_VERSION="${PREFIX}/share/${PKG_NAME}-${PKG_VERSION}"

PROXY_LAUNCHER_NAME="proxy-launcher"
PROXY_LAUNCHER="${PKG_FULL_HOME_PATH}/bin/${PROXY_LAUNCHER_NAME}"

mkdir -vp ${PREFIX}/bin;
mkdir -vp ${PREFIX}/share;
mkdir -vp ${PKG_FULL_HOME_PATH_VERSION};

# Move source to /share/{pkg}-{version}
cp -va ${SRC_DIR}/* ${PKG_FULL_HOME_PATH_VERSION} || exit 1;

# Link /share/{pkg} to /share/{pkg}-{version}
pushd ${PREFIX}/share || exit 1;
ln -sv ${PKG_NAME}-${PKG_VERSION} ${PKG_NAME} || exit  1;
popd || exit 1;

# Create proxy-launcher script that will call the pkg binaries
# proxy-launcher recives one binary as argument and executes it with the correct variables
cat > ${PROXY_LAUNCHER} <<EOF
#!/bin/bash

CWD="\$(cd "\$(dirname "\${0}")" && pwd -P)"
CMD="\$(basename "\${0}")"

export SCALA_HOME="\$(cd "\${CWD}/../share/${PKG_NAME}" && pwd -P)"
echo -e "Setting up SCALA_HOME to \${SCALA_HOME} ..."

if [[ -z \${@} ]]; then
    echo -e "Launching \${CMD}"
    echo -e ""
    \${SCALA_HOME}/bin/\${CMD}
else
    echo -e "Launching \${CMD} \"\${@}\""
    echo -e ""
    \${SCALA_HOME}/bin/\${CMD} "\${@}"
fi
EOF
chmod 755 ${PROXY_LAUNCHER} || exit 1;

# Link from `/bin/{pkg-binary}` to `/share/pkg/bin/proxy-launcher {pkg-binary}`
BIN_ITEM_LIST="$(cd ${PKG_FULL_HOME_PATH}/bin && ls * 2>/dev/null)"
pushd ${PREFIX}/bin/ || exit 1;
for item in ${BIN_ITEM_LIST}; do
    ln -vs ../share/${PKG_NAME}/bin/${PROXY_LAUNCHER_NAME} ${item} || exit 1;
done
popd || exit 1;

# Remove proxy-launcher from environment `bin` directory, it will still be on /share/pkg/bin/proxy-launcher
rm -v ${PREFIX}/bin/${PROXY_LAUNCHER_NAME} || exit 1;
