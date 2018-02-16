class CreateRecognizes < ActiveRecord::Migration[5.1]
  def change
    create_table :recognizes do |t|
      t.string :attachment

      t.timestamps
    end
  end
end
