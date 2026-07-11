# Document-Driven Form Builder Proposal
This document proposes an approach to creating a document-driven form builder through iterative stages. 

# Bet
Create a document-driven form builder.

## Details
By "document-driven" we mean a user may upload a structured document.

The form builder then takes this document and transforms it into a form which can be used by an author to complete 
tasks.

## Reason
- Creating forms and associated logic for forms is tedious and repetitive for developers.
- Forms are often subject to change by groups outside digital .
- Documents can be reused in different journals or (production, staging, development) environments to enable easier 
  content transfers.

## Definitions
The following define certain terms used within the document
- input type 
  - will refer to an HTML type form input as defined in the following section ("Input Types")
- Form Document
  - Refers to the structured document uploaded by a user which represents a form or segment of a form
- Form Models
  - Refers to the Django models which represent the form data captured by the form document
  - Used for rendering the HTML and logic of the form views 

### Input Types
| Input Type | Description                                                                                             | Example Code                                           |
|------------|---------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| text       | A single-line text field for user input. Default type if none is specified.                             | `<input type="text" name="username">`                  |
| paragraph | A multi-line text field for user input.                                                                 |                                                        |
| selection | A drop down selection box for user input.                                                               |                                                        |
| password	  | A text field that obscures user input, typically used for passwords.                                    | `<input type="password" name="password">`              |
| email      | A field for entering email addresses, with validation to ensure proper format                           | `<input type="email" name="email">`                    |
| number     | Allows numeric input with optional validation for range and step values.                                | `<input type="number" name="age" min="0">`             |
| checkbox   | A box that can be checked or unchecked, allowing multiple selections.                                   | `<input type="checkbox" name="subscribe">`             |
| radio      | Allows selection of one option from a set of choices. Only one radio button in a group can be selected. | `<input type="radio" name="gender" value="male">`      |
| file	      | Enables users to upload files from their device.                                                        | `<input type="file" name="upload">`                    |
| date	      | A field for selecting a date, often with a date picker interface.                                       | `<input type="date" name="birthday">`                  |
| color      | A control for selecting a color, typically opens a color picker.                                        | `<input type="color" name="favcolor">`                 |
| range      | A slider control for selecting a numeric value within a specified range.                                | `<input type="range" name="volume" min="0" max="100">` |
| search     | A text field optimized for search queries, often styled differently by browsers.                        | `<input type="search" name="query">`                   |
| submit     | A button that submits the form data to the server.                                                      | `<input type="submit" value="Submit">`                 |
| reset      | A button that resets all form fields to their default values.                                           | `<input type="reset" value="Reset">`                   |
| hidden     | A field that is not visible to users but holds data to be submitted with the form.                      | `<input type="hidden" name="userId" value="123">`      |

### Built-in Validation Types

The following validation types are supported for different input types:

1. **min_length / max_length**: For text inputs (text, paragraph, password, search, hidden)
   - min_length: Minimum number of characters
   - max_length: Maximum number of characters
2. **min_value / max_value**: For number inputs (number, range)
   - min_value: Minimum allowed value
   - max_value: Maximum allowed value
3. **pattern**: Regex pattern matching for text inputs (text, paragraph, password, search, hidden)
4. **required**: Enhanced version of the existing "Required" parameter, applicable to all inputs
5. **email**: Email format validation for email inputs
6. **url**: URL format validation for URL inputs
7. **custom**: For complex custom validation logic
8. **min_date / max_date**: For date inputs
   - min_date: Earliest allowed date
   - max_date: Latest allowed date
9. **format**: Expected format for date, color, and hidden inputs
10. **enum**: List of allowed values for selection, checkbox groups, and radio inputs
11. **file_types / max_size**: For file inputs
    - file_types: Allowed file extensions or MIME types
    - max_size: Maximum file size in bytes
12. **min_checked / max_checked**: For checkbox groups
    - min_checked: Minimum number of checkboxes that must be checked
    - max_checked: Maximum number of checkboxes that can be checked
13. **step**: Increment/decrement step value for number and range inputs

### Integration with Existing Features

1. The validation parameter works with the existing "Required" parameter and can potentially enhance or replace it
2. Validation integrates with the "Logic" parameter to allow conditional validation
3. Validation supports all input types defined in the specification

# Stage 1
Stage 1 is meant to create a prototype which tests the viability of the approach.

## Acceptance Criteria for Stage 1.1 (Document Structure)
- Decide which type of document to use for structuring the information required for a form document
  - Our options: 
    - XML
    - YAML
    - JSON
  - Decision criteria
    - Native support in Python/Django
    - Schema validation capabilities   
- The structure of the form document should be defined with code somehow
  - Some sort of linting should exist which defines what values are/n't allowed
- The structure of the form document should include at least the following
  - Variable
    - Description: An object which holds values used within the logic. Variables given a save pathway will save 
      their values at the end of the form process which may override values from the input. All variables are 
      referenced by using `{scope.[VARIABLE ID]}` so there is no need to add `scope.` to the ID value. 
    - Parameters
      - ID
        - Literal type: str
        - Required: True
        - Description: The id used to reference this value. 
      - Type
        - Literal type: str
          - Default: "any"
        - Required: False
        - Description: The python literal type for the given object. Defaults to "any". May define the variable 
          could be multiple types such as "str | None"
      - Value
        - Literal type: any
        - Required: True
        - Description: The starting value for the variable. May get the values from existing objects such as "
          {article.title}". 
    - Examples
      - Example 1
        - Variable
          - ID: "thank_you_message"
          - Type: "str"
          - Value: "Thank you for submitting to PLOS!"
      - Example 2
        - Variable
          - ID: "thank_you_message"
          - Type: "str | None"
          - Value: None
  - Input
    - Description: The "Input" object 
    - Parameters
      - ID
        - Literal Type: str
        - Required: False
        - Description: The id for the input (literally the `id="[value]"` of an HTML tag)
      - Name
        - Literal Type: str
        - Required: False
        - Description: The name for the input (literally the `name="[value]"` of an HTML tag)
      - Type
        - Literal Type: str
          - ["text", "paragraph", "date", "selection", "number"]
        - Required: True
        - Description: The type of input which the user is expected to enter 
      - Enum
        - Literal Type: list[any]
        - Required: False
        - Description: A list of restricted input choices 
      - Label
        - Literal Type: str
        - Required: False
        - Description: The label for the input
      - Help Text
        - Literal Type: str
        - Required: False
        - Description: The help text for the input
      - Value
        - Literal Type: any
        - Required: False
        - Description: Allows the user to set a value for the input, useful for hidden variables use in logic sections.
      - Default Value
        - Literal Type: any
        - Required: False
        - Description: The default value for the input if the user does not enter one
      - Placeholder Value
        - Literal Type: str
        - Required: False
        - Description: The placeholder value for the user to show an example of what is required for the input
      - Required
        - Literal Type: bool
          - Default: False
        - Required: False
        - Description: True if the input requires the user to enter some value, false otherwise.
      - Hidden
        - Literal Type: bool
          - Default: False
        - Required: False
        - Description: True if the input is hidden or not rendered on the page, false otherwise.
      - Variable To Save As
        - Literal Type: str
        - Required: True
        - Description: The name of the variable to save as, may have dots in name such as "article.title" to 
          represent saving the title of an article object.
      - Logic
        - Literal Type: code
        - Required: False
        - Description: This will be conditional logic yet undefined which allows the user to specify if any of the 
          previous input parameters change based upon conditional logic which may include using the IDs of other 
          inputs for the purpose of gathering their values and changing the logic based upon the values of those 
          inputs. Additionally, it may allow other values to be changed based upon the input. The value of the given 
          input is represented as "{value}". 
        - Example
          - Example 1
            - Variable
              - ID: "thank_you_message"
              - Type: "str"
              - Value: "Thank you for submitting to PLOS!"
            - Input
              - ID: "keeper"
              - Type: "number"
              - Value: 4
            - Input
              - Variable To Save As: article.journal
              - Label: "Journal to submit to"
              - Type: "selection"
              - Enum: ["PLOS One", "PLOS Bio", "Open Library of Humanities"]
              - Logic
                - not {article.type} is "research_article"
                  - then
                    - Required: True
                - {article.category} is 1
                  - then
                    - Enum: ["PLOS Water", "PLOS Bio"]
                    - {scope.keeper}
                      - Value: 5
                - {value} is "PLOS Bio"
                  - then
                    - {scope.keeper}
                      - Value: 3
                  - else {value} is "Open Library of Humanities"
                    - {scope.thank_you_message}
                      - Value: "Thank you for submitting to the Open Library of Humanities!"
                  - else
                    - {scope.keeper}
                      - Value: 1
      - Validation
        - Literal Type: list of validation rules
        - Required: False
        - Description: A list of validation rules that apply to this input. Each rule defines conditions and error 
          messages for validation.
        - Structure:
          - Rule Type: The type of validation rule (e.g., "min_length", "max_length", "pattern", "custom")
          - Rule Parameters: Parameters for the rule (e.g., minimum value, regex pattern)
          - Error Message: Custom error message for when the validation fails
          - Condition: Optional condition for when the validation should apply
        - Example:
          - Validation:
            - Rule:
              - Type: "min_length"
              - Value: 5
              - Error: "Title must be at least 5 characters long"
            - Rule:
              - Type: "pattern"
              - Value: "^[A-Z].*"
              - Error: "Title must start with a capital letter"
            - Conditional Rule:
              - Condition: "{article.type} is 'research_article'"
              - Rule:
                - Type: "max_length"
                - Value: 200
                - Error: "Research article titles must be no more than 200 characters"

## Acceptance Criteria for Stage 1.2 (Implementation)
- User can upload a form document (XML, YAML, or JSON) 
  - Form document type decided on in Stage 1.1
- The form document is limited to only the "text" input 
- Uploaded form document is transformed into Django Models (henceforth referred to as “form models”) which capture 
  data from the form document
- Information a user enters into the newly created (simplified) form mentioned previously is able to be saved in 
  Janeway’s article model.