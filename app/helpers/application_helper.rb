module ApplicationHelper
  def display_flash
    capture_haml do
      flash.each do |type, message|
        message_class = case type
        when 'notice'
          'success'
        when 'alert'
          'warning'
        when 'error'
          'danger'
        else
          'info'
        end
        haml_tag :div, class: "alert alert-#{message_class} fade in" do
          haml_tag :a, '&times;'.html_safe, class: 'close', "data-dismiss" => "alert", "aria-label" => "close"
          haml_concat message
        end
      end
    end
  end
end
