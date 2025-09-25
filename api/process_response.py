class ProcessResponse:
    trash_text = {
        '```', '~~~',
        '```python', '```python3', '```py', '```python3.x',
        '```python3.8', '```python3.9', '```python3.10', '```python3.11',
        '```python3.12', '```py3', '```py3.10', '```c',
        '```cpp', '```c++', '```c++11', '```c++14',
        '```c++17', '```c++20', '```javascript', '```js',
        '```ecmascript', '```node', '```nodejs', '```typescript',
        '```ts', '```html', '```html5', '```xhtml',
        '```css', '```css3', '```java', '```javac',
        '```go', '```golang', '```rust', '```rs',
        '```ruby', '```rb', '```php', '```php8',
        '```bash', '```sh', '```shell', '```terminal',
        '```zsh', '```fish', '```sql', '```mysql',
        '```postgresql', '```sqlite', '```json', '```javascript-object-notation',
        '```yaml', '```yml', '```xml', '```xaml',
        '```dockerfile', '```docker', '```kubernetes', '```k8s',
        '```hcl', '```terraform', '```powershell', '```ps',
        '```ps1', '```swift', '```kotlin', '```kt',
        '```scala', '```r', '```rstats', '```perl',
        '```pl', '```lua', '```dart', '```elixir',
        '```ex', '```haskell', '```hs', '```asm',
        '```assembly', '```diff', '```patch', '```log',
        '```text', '```txt', '```plain', '```ini',
        '```conf', '```configuration', '```env', '```.env',
        '```markdown', '```md', '```latex', '```tex',
    }
    
    @staticmethod
    def clean_response(response: str) -> str:
        lines = response.splitlines()
        
        if not lines: return ''

        if lines[0].strip() in ProcessResponse.trash_text:
            lines = lines[1:]
        if lines and lines[-1].strip() in ProcessResponse.trash_text:
            lines = lines[:-1]

        return '\n'.join(lines)