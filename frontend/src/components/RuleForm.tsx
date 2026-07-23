import React from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { useRuleStore } from '../services/state';
import type { Rule } from '../services/state';
import { Trash2, Plus, Save } from 'lucide-react';

type FormValues = {
  rules: Rule[];
};

export const RuleForm: React.FC = () => {
  const { rules, setRules } = useRuleStore();

  const { register, control, handleSubmit, reset } = useForm<FormValues>({
    defaultValues: { rules }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "rules"
  });

  React.useEffect(() => {
    reset({ rules });
  }, [rules, reset]);

  const onSubmit = (data: FormValues) => {
    setRules(data.rules);
    alert('Rules saved to global state!');
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="rule-form">
      {fields.length === 0 && (
        <div className="empty-state">No rules extracted yet. Upload a document or add one manually.</div>
      )}
      <div className="rules-list">
        {fields.map((field, index) => (
          <div key={field.id} className="rule-card glass-panel fade-in">
            <div className="rule-header">
              <input 
                {...register(`rules.${index}.title` as const)} 
                className="rule-title-input"
                placeholder="Rule Title"
              />
              <button 
                type="button" 
                onClick={() => remove(index)}
                className="icon-button danger"
                title="Remove Rule"
              >
                <Trash2 size={18} />
              </button>
            </div>
            <textarea 
              {...register(`rules.${index}.description` as const)} 
              className="rule-desc-input"
              placeholder="Rule Description"
              rows={3}
            />
          </div>
        ))}
      </div>
      
      <div className="form-actions">
        <button 
          type="button" 
          onClick={() => append({ id: Math.random().toString(), title: '', description: '' })}
          className="btn outline"
        >
          <Plus size={18} /> Add Rule Manually
        </button>
        <button type="submit" className="btn primary">
          <Save size={18} /> Save Changes
        </button>
      </div>
    </form>
  );
};
