#!/bin/bash

PKG_FULL_HOME_PATH="${PREFIX}/share/${PKG_NAME}"
PKG_FULL_HOME_PATH_VERSION="${PREFIX}/share/${PKG_NAME}-${PKG_VERSION}"
LAUNCHER="${PREFIX}/bin/livy-server"

mkdir -vp ${PREFIX}/bin;
mkdir -vp ${PREFIX}/share;
mkdir -vp ${PKG_FULL_HOME_PATH_VERSION};

# Move source to /share/apache-livy-version
cp -va ${SRC_DIR}/* ${PKG_FULL_HOME_PATH_VERSION} || exit 1;

# Link /share/apache-livy-version to /share/apache-livy
pushd ${PREFIX}/share || exit 1;
ln -sv ${PKG_NAME}-${PKG_VERSION} ${PKG_NAME} || exit  1;
popd || exit 1;

# Build. on /share/apache-livy
pushd ${PKG_FULL_HOME_PATH} || exit 1;
mvn package -pl '!python-api' -DskipTests
popd || exit 1;

# Create /bin/livy-server that launches the one on /share/apache-livy/bin with correct variables
cat > ${LAUNCHER} <<EOF
#!/bin/bash

CWD="\$(cd "\$(dirname "\${0}")" && pwd -P)"
CMD="\$(basename "\${0}")"

export LIVY_HOME="\$(cd "\${CWD}/../share/${PKG_NAME}" && pwd -P)"

echo -e ""
echo -e "Setting up LIVY_HOME to \${LIVY_HOME} ..."
if [[ -z \${@} ]]; then
    echo -e "Launching \${CMD}"
    echo -e ""
    \${LIVY_HOME}/bin/\${CMD}
else
    echo -e "Launching \${CMD} \"\${@}\""
    echo -e ""
    \${LIVY_HOME}/bin/\${CMD} "\${@}"
fi
EOF

chmod 755 ${LAUNCHER} || exit 1;

# clean only classes directories
pushd ${PKG_FULL_HOME_PATH} || exit 1;
find . -name "classes" | xargs rm -rf
find . -name "test-classes" | xargs rm -rf
popd || exit 1;
