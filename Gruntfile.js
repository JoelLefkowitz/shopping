module.exports = (grunt) => {
  grunt.initConfig(config);
  grunt.loadNpmTasks("grunt-exec");
  grunt.registerTask(
    "lint",
    "Lint the source code",
    toExecs(["cspell", "remark", "pylint", "bandit", "mypy"])
  );
  grunt.registerTask(
    "format",
    "Format the source code",
    toExecs(["prettier", "black", "isort", "autoflake"])
  );
  grunt.registerTask("test", "Run all unit and bdd tests", toExecs(["tox"]));
};

const toExecs = (arr) => arr.map((i) => "exec:".concat(i));

const config = {
  exec: {
    autoflake: `autoflake . -ri
              --exclude 'venv, conftest.py'
              --remove-all-unused-imports
              --remove-unused-variables
              --ignore-init-module-imports`,
    bandit: "bandit -c .bandit -r src",
    black: "black .",
    cspell: 'npx cspell ".*" "*" "**/*"',
    isort: "isort .",
    mypy: "mypy .",
    prettier: "prettier . --ignore-path ../.gitignore --write",
    pylint: "pylint --rcfile .pylintrc  --fail-under=8 src tests",
    remark: "npx remark -r .remarkrc .",
    tox: "tox .",
  },
};
