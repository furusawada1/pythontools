require 'ceedling/plugin'
require 'ceedling/constants'
class Valgrind < Plugin

  attr_reader :config

  def setup
    @config = {
      :xmlFile => ((defined? VALGRIND_XML_FILE) ? VALGRIND_XML_FILE : "valgrind.log"),
    }
    @plugin_root = File.expand_path(File.join(File.dirname(__FILE__), '..'))
  end

  def pre_test_fixture_execute(arg_hash)
    cmd = 'valgrind'
    cmd += " --track-origins=yes"
    cmd += " --trace-children=yes"
    cmd += " --leak-check=full"
    cmd += " --show-leak-kinds=all"
    cmd += " --errors-for-leak-kinds=all"
    cmd += " --error-exitcode=0"
    if (defined? VALGRIND_XML_FILE)
      cmd += " --xml=yes --xml-file=#{arg_hash[:executable]}.xml"
    else
      cmd += " --log-file=#{arg_hash[:executable]}.log"
    end
    cmd += " "
    cmd += arg_hash[:executable]
    shell_result = @ceedling[:tool_executor].exec(cmd)
    arg_hash[:shell_result] = 0
  end

  def pre_build
    cmd = 'rm'
    cmd += " -f"
    cmd += " ./build/test/out/*.out.xml"
    cmd += " ./build/test/out/*.out.log"
    cmd += " ./build/doxygen/xml/*.*"
    cmd += " ./build/unitTestList/testlist.csv"
    @ceedling[:tool_executor].exec(cmd)
  end

  def post_build
    cmd = 'python3'
    cmd += " ../tool/unitTestXmltoCsv.py"
    @ceedling[:tool_executor].exec(cmd)
  end

  def post_error
    #TODO Summarize Results
  end

end
