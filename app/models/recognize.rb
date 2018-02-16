class Recognize < ApplicationRecord
  mount_uploader :attachment, OpencvUploader
end
